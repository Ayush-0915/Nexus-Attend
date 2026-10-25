# NEXUS Attend

> **Attendance, but make it actually painless.**

NEXUS Attend is an AI-assisted attendance management platform for classrooms. Students can create a profile and sign in with FaceID, teachers can manage subjects and attendance sessions, and voice-enabled classrooms can use spoken attendance as an additional recognition method.

Built with **Python + Streamlit + Supabase**, the app keeps the experience simple for users while handling the not-so-simple parts behind the scenes: face embeddings, voice embeddings, subject enrollment, attendance logs, password hashing, and review-before-save workflows.

## What is the vibe?

- **No attendance sheet chaos:** replace manual roll call with AI-assisted workflows.
- **Two clean portals:** one for students, one for teachers.
- **Face-first login:** students can register and return using a camera snapshot.
- **Voice-ready attendance:** teachers can analyze classroom audio when students have voice profiles.
- **QR/link enrollment:** share one subject code or join link and move on.
- **Human-in-the-loop:** detected attendance is shown for review before it is saved.
- **Cloud-backed:** Supabase stores users, subjects, enrollments, and attendance records.

## Features

### Student portal

- Create a student profile with a name and face profile.
- Optionally record a voice sample during registration.
- Log in with a camera capture and face recognition.
- Enroll in a subject using a teacher-provided subject code.
- Join a subject through a shared `join-code` link.
- View enrolled subjects and attendance totals.
- Unenroll from a subject.
- Log out securely from the active session.

### Teacher portal

- Register with a username, name, and password.
- Log in with password authentication.
- Create and manage subjects.
- View enrollment and class activity summaries.
- Share subject codes and QR-enabled join links.
- Take attendance from one or more classroom photos using face recognition.
- Take attendance from classroom audio using voice recognition.
- Review detected results before saving them.
- View attendance records in a tabular dashboard.

### Recognition pipelines

- **Face pipeline:** Dlib detects faces and creates 128-dimensional face embeddings. A linear SVM classifies known student embeddings, followed by a distance threshold check.
- **Voice pipeline:** Resemblyzer creates voice embeddings from audio. Cosine similarity is used to identify enrolled speakers.
- Models are cached with Streamlit resources to avoid reloading them on every interaction.

## Tech stack

| Area | Technology |
| --- | --- |
| UI and app runtime | Streamlit |
| Language | Python |
| Database and API | Supabase |
| Password security | `bcrypt` |
| Face detection and embeddings | `dlib`, `face_recognition_models` |
| Face classification | `scikit-learn` |
| Audio processing | `librosa` |
| Voice embeddings | `resemblyzer` |
| Images and arrays | Pillow, NumPy |
| Data tables | pandas |
| QR generation | segno |

## Project structure

```text
NEXUS Attend/
├── app.py                         # Streamlit entry point and routing
├── requirements.txt               # Python dependencies
├── .streamlit/
│   └── secrets.toml               # Local secrets; never commit this file
└── src/
    ├── components/                # Dialogs, cards, headers, and footer UI
    ├── database/
    │   ├── config.py              # Supabase client initialization
    │   └── db.py                  # Database operations and auth helpers
    ├── pipelines/
    │   ├── face_pipeline.py       # Face embeddings and recognition
    │   └── voice_pipeline.py      # Voice embeddings and recognition
    ├── screens/
    │   ├── home_screen.py         # Portal selection
    │   ├── student_screen.py      # Student login and dashboard
    │   └── teacher_screen.py      # Teacher auth and dashboard
    └── ui/
        └── style_base_layout.py   # Shared Streamlit styling
```

## Requirements

### Software

- Python **3.10 or newer**. Python 3.11 is a practical baseline for the computer-vision/audio dependencies.
- A Supabase project.
- A working camera for FaceID flows.
- A microphone for voice enrollment or voice attendance.
- On Windows, install the required native Python wheels in a supported Python environment. `dlib` is the dependency most likely to need platform-specific troubleshooting.

### Supabase tables

The application expects these tables and relationships:

| Table | Important columns |
| --- | --- |
| `teachers` | `teacher_id`, `username`, `password`, `name` |
| `students` | `student_id`, `name`, `face_embedding`, `voice_embedding` |
| `subjects` | `subject_id`, `subject_code`, `name`, `section`, `teacher_id` |
| `subject_students` | `student_id`, `subject_id` |
| `attendance_logs` | `student_id`, `subject_id`, `timestamp`, `is_present` |

Recommended database rules:

- Make primary keys unique and auto-generated where appropriate.
- Make `teachers.username` and `subjects.subject_code` unique.
- Add foreign keys from `subjects.teacher_id`, `subject_students`, and `attendance_logs`.
- Prevent duplicate `(student_id, subject_id)` rows in `subject_students`.
- Store embeddings in a format Supabase can return as a JSON-compatible array, such as `jsonb`.
- Restrict database access with Supabase Row Level Security before deploying publicly.

> The repository does not currently include a Supabase migration file. Create the schema in Supabase before starting the app, and match the column names above exactly.

## Local setup

### 1. Clone the repository

```bash
git clone https://github.com/Ayush-0915/NEXUS-Attend.git
cd NEXUS-Attend
```

### 2. Create and activate a virtual environment

**Windows PowerShell**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS/Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If the face-recognition dependencies fail to install, use a supported Python version and confirm that a compatible `dlib-bin` wheel exists for your operating system.

### 4. Add Supabase secrets

Create `.streamlit/secrets.toml` locally:

```toml
SUPABASE_URL = "https://your-project-ref.supabase.co"
SUPABASE_KEY = "your-supabase-key"
```

Never commit real credentials. `.streamlit/secrets.toml` is ignored by Git in this project.

### 5. Start the app

```bash
streamlit run app.py
```

Open the local URL shown by Streamlit, usually `http://localhost:8501`.

## Typical user flows

### Student flow

1. Select **Student Portal**.
2. Position one face in the camera frame.
3. For a new student, enter a name and optionally record a voice sample.
4. After login, select **Enroll in Subject**.
5. Enter the subject code or open a teacher's join link.
6. Review subject attendance from the student dashboard.

### Teacher flow

1. Select **Teacher Portal**.
2. Register or log in.
3. Create a subject with a code, name, and section.
4. Share the subject code or QR join link.
5. Open **Take Attendance**.
6. Add classroom photos and run face analysis, or use voice attendance.
7. Review the detected students.
8. Confirm and save the attendance session.
9. Check **Attendance Records** for the stored results.

## Configuration and recognition thresholds

The current recognition behavior is defined in the source code:

- Face matching uses a distance threshold of `0.6` in `src/pipelines/face_pipeline.py`.
- Voice matching uses a cosine-similarity threshold of `0.55` in `src/pipelines/voice_pipeline.py`.
- Voice recognition only considers audio segments that are at least approximately `0.3` seconds long.

These values affect false positives and false negatives. Tune them with real classroom data, document any changes, and always keep the review-before-save step enabled.

## Security and privacy

NEXUS Attend processes biometric-like data: face embeddings, voice embeddings, camera images, and audio recordings. Treat this data as sensitive.

- Use HTTPS in production.
- Keep Supabase keys in Streamlit secrets or deployment environment variables.
- Never commit `.streamlit/secrets.toml`, raw recordings, or generated embeddings.
- Enable Supabase Row Level Security and write policies for every table.
- Limit teacher access to subjects they own.
- Limit students to their own profile, enrollments, and attendance data.
- Use a clear retention and deletion policy for biometric profiles.
- Get informed consent before collecting face or voice data.
- Provide a non-biometric attendance alternative where required by school policy or local law.
- Remember that a successful recognition result is not proof of identity. Keep teacher review and auditability in the loop.

## Troubleshooting

### `KeyError: SUPABASE_URL` or `SUPABASE_KEY`

Create `.streamlit/secrets.toml` and add both values. Restart Streamlit after changing secrets.

### `dlib` or face model installation errors

Use Python 3.11, update `pip`, and install inside a clean virtual environment. Native wheels vary by Python version and operating system.

### The app starts but database actions fail

Check the Supabase URL, key, table names, column names, foreign keys, and Row Level Security policies. The app expects the schema listed in this README.

### A face is not recognized

- Use good, even lighting.
- Keep exactly one face in the frame.
- Capture a clear, front-facing image.
- Confirm the student has a stored face embedding.
- Retrain the cached classifier after adding profiles by restarting the app or using the registration flow.

### Voice recognition returns no matches

- Confirm enrolled students have voice profiles.
- Record clear audio with low background noise.
- Make sure students speak long enough for a usable segment.
- Check the microphone permissions in the browser.

## Deployment

Streamlit Community Cloud is a natural deployment target:

1. Push the repository to GitHub.
2. Create a new Streamlit app from the repository.
3. Set the main file to `app.py`.
4. Add `SUPABASE_URL` and `SUPABASE_KEY` in the app's Secrets settings.
5. Confirm your Supabase schema and security policies.
6. Test camera, microphone, enrollment, and attendance review in the deployed URL.

For any production host, verify that the host supports the native dependencies used by `dlib`, audio processing, and Resemblyzer.

## Development notes

- Streamlit session state controls portal selection and active login state.
- Supabase is initialized at import time from `st.secrets`.
- Face and voice model loading is cached with `st.cache_resource`.
- Attendance is written only after a teacher confirms the review table.
- Generated runtime files, local databases, uploads, cache data, and biometric artifacts are ignored by Git.

## Roadmap ideas

- Add database migrations and seed data.
- Add automated tests for auth, enrollment, recognition thresholds, and attendance writes.
- Add confidence scores and teacher override controls.
- Add CSV export and date/subject filters for reports.
- Add duplicate-session protection.
- Add audit logs and explicit consent/retention controls.
- Add a password reset flow and stronger session management.

## Contributing

1. Create a focused branch.
2. Keep changes small and explain behavior changes.
3. Do not include secrets, raw biometric data, or generated model files.
4. Run the app locally and test both teacher and student flows.
5. Open a pull request with a clear summary and screenshots for UI changes.

## License

No license file is currently included. Until a license is added, all rights remain with the repository owner and reuse should be confirmed before redistribution.

---

Made for classrooms that have better things to do than yell, “Present?” 30 times. ✨
