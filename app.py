import os
import uuid
import smtplib
from email.mime.text import MIMEText
from datetime import timedelta
from functools import wraps

# Loads variables from a local .env file during development.
# On Render, real environment variables are already set in the dashboard,
# so this simply finds no .env file there and does nothing — safe either way.
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from flask import (
    Flask, render_template, request, redirect, Response,
    session, url_for, flash
)
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from supabase import create_client, Client

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-change-me")
app.permanent_session_lifetime = timedelta(days=180)  # "stay logged in" window

# ---------------------------------------------------------------------------
# Supabase setup. Set these as env vars on Render:
#   SUPABASE_URL, SUPABASE_KEY (service_role key), ADMIN_PASSWORD, SECRET_KEY
# ---------------------------------------------------------------------------
SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_KEY"]
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

BUCKET = "exam-papers"
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "changeme")
ALLOWED_EXTENSIONS = {"pdf", "jpg", "jpeg", "png"}

# ---------------------------------------------------------------------------
# Email setup (for verification + password reset links). Set these as env
# vars on Render. See SETUP_GUIDE for how to get a Gmail "App Password".
#   SMTP_HOST (e.g. smtp.gmail.com), SMTP_PORT (e.g. 587)
#   SMTP_USERNAME, SMTP_PASSWORD, FROM_EMAIL (defaults to SMTP_USERNAME)
# ---------------------------------------------------------------------------
SMTP_HOST = os.environ.get("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
SMTP_USERNAME = os.environ.get("SMTP_USERNAME")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD")
FROM_EMAIL = os.environ.get("FROM_EMAIL", SMTP_USERNAME)

serializer = URLSafeTimedSerializer(app.secret_key)
EMAIL_VERIFY_SALT = "email-verify"
PASSWORD_RESET_SALT = "password-reset"

YEAR_META = {
    "1st": {
        "title": "First Year Papers",
        "description": "Discover the foundation of engineering with introductory courses.",
        "number": 1,
        "subjects": [
            "Maths1", "Physics", "Soft Skills", "PPS", "Chemistry",
            "Environment", "Maths2", "Mechanical Engineering",
            "Electrical Engineering", "Electronics Engineering",
        ],
    },
    "2nd": {
        "title": "Second Year Papers",
        "description": "Dive deeper into your core subjects and practical learning and clear your basics.",
        "number": 2,
        "subjects": [
            "Data Structures", "Automata", "Technical Comm.", "Cyber Security",
            "Digital Electronics", "Computer Org. & Arch.", "Discrete Maths",
            "Operating System", "Human Values", "Python", "Java", "Maths - IV",
        ],
    },
    "3rd": {
        "title": "Third Year Papers",
        "description": "Master advanced topics and prepare for internships and projects.",
        "number": 3,
        "subjects": [
            "Web Technology", "Machine Learning", "Data Analytics", "Algorithms",
            "Constitution", "DBMS", "Compiler Design", "Computer Network",
            "SPM", "Software Engineering", "Big Data",
        ],
    },
    "4th": {
        "title": "Final Year Papers",
        "description": "Finalize your journey with specializations and your major projects.",
        "number": 4,
        "subjects": ["Machine Learning", "Cloud Computing", "AI"],
    },
}

EXAM_TYPES = ["sessional1", "sessional2", "semester"]
EXAM_TYPE_LABELS = {
    "sessional1": "Sessional 1",
    "sessional2": "Sessional 2",
    "semester": "Semester",
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("student_id"):
            flash("Please log in first.")
            return redirect(url_for("login", next=request.path))
        return view(*args, **kwargs)
    return wrapped


def send_email(to_email, subject, html_body):
    """Sends an email via SMTP. Returns True on success, False if it failed
    (never raises — a broken email shouldn't break registration/login)."""
    if not SMTP_USERNAME or not SMTP_PASSWORD:
        app.logger.warning("Email not sent (SMTP_USERNAME/SMTP_PASSWORD not set): %s", subject)
        return False
    try:
        msg = MIMEText(html_body, "html")
        msg["Subject"] = subject
        msg["From"] = FROM_EMAIL
        msg["To"] = to_email
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(FROM_EMAIL, [to_email], msg.as_string())
        return True
    except Exception as e:
        app.logger.error("Failed to send email to %s: %s", to_email, e)
        return False


def get_student(student_id):
    row = (
        supabase.table("students")
        .select("*")
        .eq("student_id", student_id)
        .execute()
    ).data
    return row[0] if row else None


def send_verification_email(student_id, email):
    token = serializer.dumps(student_id, salt=EMAIL_VERIFY_SALT)
    verify_url = url_for('verify_email', token=token, _external=True)
    html = f"""
    <p>Hi {student_id},</p>
    <p>Welcome to SIET Exams. Please verify your email to enable uploading papers:</p>
    <p><a href="{verify_url}">{verify_url}</a></p>
    <p>This link expires in 24 hours.</p>
    """
    return send_email(email, "Verify your SIET Exams account", html)


def get_approved_papers(year):
    """Returns {subject_name: {exam_type: file_url}} for approved rows of a year."""
    res = (
        supabase.table("papers")
        .select("subject, exam_type, file_url")
        .eq("year", year)
        .eq("approved", True)
        .order("created_at", desc=True)
        .execute()
    )
    by_subject = {}
    for row in res.data:
        subj = row["subject"]
        by_subject.setdefault(subj, {})
        by_subject[subj].setdefault(row["exam_type"], row["file_url"])
    return by_subject


# ---------------------------------------------------------------------------
# Static / SEO routes (unchanged from before)
# ---------------------------------------------------------------------------
@app.route('/robots.txt')
def robots_txt():
    return Response(
        "User-agent: Googlebot\nDisallow:\nSitemap: https://siet-exams.onrender.com/sitemap.xml",
        mimetype='text/plain'
    )


@app.route('/sitemap.xml')
def sitemap():
    sitemap_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
<url><loc>https://siet-exams.onrender.com/</loc><priority>1.00</priority></url>
<url><loc>https://siet-exams.onrender.com/login</loc><priority>0.80</priority></url>
<url><loc>https://siet-exams.onrender.com/register</loc><priority>0.80</priority></url>
</urlset>'''
    return Response(sitemap_xml, mimetype='application/xml')


@app.route("/feedback")
def feedback():
    return redirect(
        'https://wa.me/918920388443?text=Hi%20Sudo%2C%20I%20have%20feedback%20about%20SIET%20Exams'
    )


# ---------------------------------------------------------------------------
# Auth: register / login / logout
# ---------------------------------------------------------------------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if session.get('student_id'):
        return redirect(url_for('dashboard'))

    if request.method == 'GET':
        return render_template('register.html')

    student_id = (request.form.get('student_id') or '').strip()
    email = (request.form.get('email') or '').strip().lower()
    mobile_number = (request.form.get('mobile_number') or '').strip()
    password = request.form.get('password') or ''
    confirm_password = request.form.get('confirm_password') or ''

    if not student_id or not email or not mobile_number or not password:
        flash("Please fill in all fields.")
        return redirect(url_for('register'))
    if password != confirm_password:
        flash("Passwords don't match.")
        return redirect(url_for('register'))
    if len(password) < 6:
        flash("Password must be at least 6 characters.")
        return redirect(url_for('register'))

    existing = (
        supabase.table("students")
        .select("id")
        .eq("student_id", student_id)
        .execute()
    ).data
    if existing:
        flash("That Student ID is already registered. Try logging in instead.")
        return redirect(url_for('login'))

    existing_email = (
        supabase.table("students")
        .select("id")
        .eq("email", email)
        .execute()
    ).data
    if existing_email:
        flash("That email is already registered. Try logging in instead.")
        return redirect(url_for('login'))

    supabase.table("students").insert({
        "student_id": student_id,
        "email": email,
        "mobile_number": mobile_number,
        "password_hash": generate_password_hash(password),
        "email_verified": False,
    }).execute()

    session.permanent = True
    session['student_id'] = student_id

    if send_verification_email(student_id, email):
        flash("Welcome! We've sent a verification link to your email — verify it to unlock uploading.")
    else:
        flash("Welcome! (We couldn't send a verification email right now — you can resend it from your dashboard.)")

    return redirect(url_for('dashboard'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('student_id'):
        return redirect(url_for('dashboard'))

    if request.method == 'GET':
        return render_template('login.html')

    student_id = (request.form.get('student_id') or '').strip()
    password = request.form.get('password') or ''

    row = (
        supabase.table("students")
        .select("student_id, password_hash")
        .eq("student_id", student_id)
        .execute()
    ).data

    if not row or not check_password_hash(row[0]['password_hash'], password):
        flash("Incorrect Student ID or password.")
        return redirect(url_for('login'))

    session.permanent = True
    session['student_id'] = row[0]['student_id']
    next_url = request.args.get('next') or url_for('dashboard')
    return redirect(next_url)


@app.route('/logout')
def logout():
    session.pop('student_id', None)
    return redirect(url_for('login'))


# ---------------------------------------------------------------------------
# Email verification
# ---------------------------------------------------------------------------
@app.route('/verify-email/<token>')
def verify_email(token):
    try:
        student_id = serializer.loads(token, salt=EMAIL_VERIFY_SALT, max_age=86400)
    except SignatureExpired:
        flash("That verification link expired. Request a new one below.")
        return redirect(url_for('dashboard') if session.get('student_id') else url_for('login'))
    except BadSignature:
        flash("That verification link isn't valid.")
        return redirect(url_for('dashboard') if session.get('student_id') else url_for('login'))

    supabase.table("students").update({"email_verified": True}).eq("student_id", student_id).execute()
    flash("Your email is verified! You can now upload papers.")
    return redirect(url_for('dashboard') if session.get('student_id') else url_for('login'))


@app.route('/resend-verification')
@login_required
def resend_verification():
    student = get_student(session['student_id'])
    if not student:
        return redirect(url_for('dashboard'))
    if student.get('email_verified'):
        flash("Your email is already verified.")
        return redirect(url_for('dashboard'))

    if send_verification_email(student['student_id'], student['email']):
        flash("Verification email sent — check your inbox.")
    else:
        flash("Couldn't send the email right now. Try again shortly.")
    return redirect(url_for('dashboard'))


# ---------------------------------------------------------------------------
# Forgot / reset password
# ---------------------------------------------------------------------------
@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'GET':
        return render_template('forgot_password.html')

    email = (request.form.get('email') or '').strip().lower()
    row = (
        supabase.table("students")
        .select("student_id, email")
        .eq("email", email)
        .execute()
    ).data

    # Always show the same message, whether or not the email exists,
    # so this form can't be used to check who's registered.
    if row:
        token = serializer.dumps(row[0]['student_id'], salt=PASSWORD_RESET_SALT)
        reset_url = url_for('reset_password', token=token, _external=True)
        html = f"""
        <p>Hi {row[0]['student_id']},</p>
        <p>Click below to set a new password. This link expires in 1 hour.</p>
        <p><a href="{reset_url}">{reset_url}</a></p>
        <p>If you didn't request this, you can ignore this email.</p>
        """
        send_email(email, "Reset your SIET Exams password", html)

    flash("If that email is registered, a reset link has been sent.")
    return redirect(url_for('login'))


@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        student_id = serializer.loads(token, salt=PASSWORD_RESET_SALT, max_age=3600)
    except SignatureExpired:
        flash("That reset link expired. Request a new one.")
        return redirect(url_for('forgot_password'))
    except BadSignature:
        flash("That reset link isn't valid.")
        return redirect(url_for('forgot_password'))

    if request.method == 'GET':
        return render_template('reset_password.html', token=token)

    password = request.form.get('password') or ''
    confirm_password = request.form.get('confirm_password') or ''

    if password != confirm_password:
        flash("Passwords don't match.")
        return redirect(url_for('reset_password', token=token))
    if len(password) < 6:
        flash("Password must be at least 6 characters.")
        return redirect(url_for('reset_password', token=token))

    supabase.table("students").update({
        "password_hash": generate_password_hash(password)
    }).eq("student_id", student_id).execute()

    flash("Password updated — log in with your new password.")
    return redirect(url_for('login'))


# ---------------------------------------------------------------------------
# Dashboard + year pages
# ---------------------------------------------------------------------------
@app.route('/')
def home():
    if session.get('student_id'):
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    student = get_student(session['student_id'])
    email_verified = bool(student and student.get('email_verified'))
    return render_template('dashboard.html', year_meta=YEAR_META, email_verified=email_verified)


@app.route('/papers/<year>')
@login_required
def papers(year):
    meta = YEAR_META.get(year)
    if not meta:
        return "Year not found", 404

    papers_by_subject = get_approved_papers(year)
    subjects = []
    for name in meta["subjects"]:
        links = papers_by_subject.get(name, {})
        subjects.append({
            "name": name,
            "sessional1_link": links.get("sessional1", ""),
            "sessional2_link": links.get("sessional2", ""),
            "semester_link": links.get("semester", ""),
        })

    return render_template('year.html', year_key=year, meta=meta, subjects=subjects)


# ---------------------------------------------------------------------------
# Self-serve upload (requires login — uploader is auto-tagged)
# ---------------------------------------------------------------------------
@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    student = get_student(session['student_id'])
    if not student or not student.get('email_verified'):
        flash("Please verify your email before uploading — check your inbox, or resend the link from your dashboard.")
        return redirect(url_for('dashboard'))

    if request.method == 'GET':
        return render_template(
            'upload.html',
            year_meta=YEAR_META,
            exam_types=EXAM_TYPES,
            exam_type_labels=EXAM_TYPE_LABELS,
        )

    year = request.form.get('year')
    subject = request.form.get('subject')
    exam_type = request.form.get('exam_type')
    file = request.files.get('paper')

    def back_with_error(msg):
        flash(msg)
        return redirect(url_for('upload'))

    if year not in YEAR_META:
        return back_with_error("Please select a valid year.")
    if subject not in YEAR_META[year]['subjects']:
        return back_with_error("Please select a valid subject.")
    if exam_type not in EXAM_TYPES:
        return back_with_error("Please select a valid exam type.")
    if not file or file.filename == '':
        return back_with_error("Please choose a file to upload.")
    if not allowed_file(file.filename):
        return back_with_error("Only PDF, JPG or PNG files are allowed.")

    ext = file.filename.rsplit('.', 1)[1].lower()
    storage_path = f"{year}/{secure_filename(subject)}/{exam_type}-{uuid.uuid4().hex[:8]}.{ext}"

    file_bytes = file.read()
    supabase.storage.from_(BUCKET).upload(
        storage_path, file_bytes, {"content-type": file.mimetype}
    )
    public_url = supabase.storage.from_(BUCKET).get_public_url(storage_path)

    supabase.table("papers").insert({
        "year": year,
        "subject": subject,
        "exam_type": exam_type,
        "file_url": public_url,
        "uploaded_by": session.get('student_id'),
        "approved": False,
    }).execute()

    return render_template('upload_success.html')


# ---------------------------------------------------------------------------
# Admin approval panel (separate password, not tied to student accounts)
# ---------------------------------------------------------------------------
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST' and 'password' in request.form:
        if request.form['password'] == ADMIN_PASSWORD:
            session['is_admin'] = True
        else:
            flash("Wrong password.")
        return redirect(url_for('admin'))

    if not session.get('is_admin'):
        return render_template('admin_login.html')

    pending = (
        supabase.table("papers")
        .select("*")
        .eq("approved", False)
        .order("created_at", desc=True)
        .execute()
    ).data

    return render_template('admin.html', pending=pending, exam_type_labels=EXAM_TYPE_LABELS)


@app.route('/admin/approve/<int:paper_id>', methods=['POST'])
def admin_approve(paper_id):
    if not session.get('is_admin'):
        return redirect(url_for('admin'))
    supabase.table("papers").update({"approved": True}).eq("id", paper_id).execute()
    return redirect(url_for('admin'))


@app.route('/admin/reject/<int:paper_id>', methods=['POST'])
def admin_reject(paper_id):
    if not session.get('is_admin'):
        return redirect(url_for('admin'))
    supabase.table("papers").delete().eq("id", paper_id).execute()
    return redirect(url_for('admin'))


@app.route('/admin/logout')
def admin_logout():
    session.pop('is_admin', None)
    return redirect(url_for('admin'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
