import json
from pathlib import Path

# ponytail: baca portfolio.json langsung dari disk; upgrade ke vector store jika data > 100kb
def _build_context_from_json() -> str:
    candidates = [
        Path(__file__).resolve().parent.parent / "portfolio.json",
        Path.cwd() / "portfolio.json",
        Path("portfolio.json"),
    ]
    json_path = next((p for p in candidates if p.is_file()), None)
    if not json_path:
        return ""

    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return ""

    lines = []

    # 1. profil
    profile = data.get("profile", {})
    lines.append("=== PROFIL UTAMA ===")
    lines.append(f"Nama: {profile.get('nama', 'Fathi Fadhil')}")
    lines.append("Website: fathifadhil.me")
    lines.append(f"Fokus: {profile.get('subJudul', '').strip()}")
    lines.append("Status: Available for Work & Freelance")
    lines.append(f"Jurusan: {profile.get('jurusan', 'Teknik Informatika')}")
    lines.append(f"Email: {profile.get('email', 'fathifadhil10@gmail.com')}")
    lines.append(f"LinkedIn: {profile.get('linkedinLink', '')}")
    lines.append(f"GitHub: {profile.get('githubLink', '')}")
    lines.append(f"Instagram: {profile.get('instagramLink', '')}")
    lines.append(f"CV: {profile.get('linkCv', '')}")
    lines.append(f"WhatsApp: {data.get('contact', {}).get('whatsappNumber', '+6282241211466')}")
    lines.append(f"Deskripsi Home: {profile.get('deskripsiHome', '')}")
    lines.append(f"Deskripsi About: {profile.get('deskripsiAbout', '')}")
    lines.append(f"Motivasi: \"{profile.get('motivation', '')}\"")
    lines.append("")

    # 2. workflow
    wf = data.get("workflow", {})
    if wf:
        lines.append("=== WORKFLOW & METODOLOGI PENGEMBANGAN ===")
        lines.append(f"Judul: {wf.get('title', {}).get('id', 'Dari Ide Menjadi Produk')}")
        lines.append(f"Prinsip: {wf.get('description', {}).get('id', '')}")
        lines.append("Tahapan:")
        for step in wf.get("steps", []):
            stitle = step.get("title", {}).get("id", "")
            slead = step.get("lead", {}).get("id", "")
            sannot = step.get("annotation", {}).get("id", "")
            subs = ", ".join([sub.get("label", {}).get("id", "") for sub in step.get("subItems", [])])
            lines.append(f"- {step.get('id', '').capitalize()} ({stitle}): {slead} [{sannot}] (Fokus: {subs})")
        lines.append("")

    # 3. tech stack
    lines.append("=== TECH STACK ===")
    tech_items = [t.get("nama") for t in data.get("techStack", []) if t.get("nama")]
    lines.append(f"Keahlian Teknologi: {', '.join(tech_items)}")
    lines.append("")

    # 4. proyek
    lines.append("=== PROYEK UNGGULAN & PORTOFOLIO ===")
    for p in data.get("projects", {}).get("engineering", []):
        pid = p.get("id", "")
        title = p.get("judul", "")
        featured = " ★ Featured" if p.get("featured") else ""
        tgl = p.get("tanggal", "")
        lines.append(f"{pid}. {title} ({tgl}){featured}")

        cs = p.get("caseStudy", {})
        if cs:
            role = cs.get("role", {}).get("id", "")
            ctx = cs.get("context", {}).get("id", "")
            challenge = cs.get("challenge", {}).get("id", "")
            solution = cs.get("solution", {}).get("id", "")
            result = cs.get("result", {}).get("id", "")
            if role: lines.append(f"   - Role: {role}")
            if ctx: lines.append(f"   - Konteks: {ctx}")
            if challenge: lines.append(f"   - Tantangan: {challenge}")
            if solution: lines.append(f"   - Solusi: {solution}")
            if result: lines.append(f"   - Hasil: {result}")

        desc = p.get("deskripsi", "").split("\n\n")[0].replace("\n", " ")
        lines.append(f"   - Ringkasan: {desc}")
        lines.append(f"   - Tech Stack: {p.get('techStack', '')}")

        demo = p.get("linkDemo", "")
        repo = p.get("linkGithub", "")
        status = p.get("repositoryStatus", "")
        if demo: lines.append(f"   - Demo: {demo}")
        if repo: lines.append(f"   - GitHub: {repo}")
        elif status: lines.append(f"   - Repositori: {status.capitalize()}")
        lines.append("")

    # 5. sertifikasi
    lines.append("=== SERTIFIKASI ===")
    for c in data.get("certificates", []):
        cid = c.get("id", "")
        title = c.get("judul", "")
        pen = c.get("penerbitTempat", "")
        dur = c.get("tahunDurasi", "")
        desc = c.get("deskripsi", "")
        verif = c.get("verifikasi", "")
        lines.append(f"{cid}. {title} - {pen} ({dur})")
        if desc: lines.append(f"   - Deskripsi: {desc}")
        if verif: lines.append(f"   - Kredensial/Verifikasi: {verif}")
    lines.append("")

    # 6. pengalaman
    lines.append("=== PENGALAMAN ===")
    for exp in data.get("experience", []):
        eid = exp.get("id", "")
        judul = exp.get("judul", {}).get("id", "")
        tempat = exp.get("penerbitTempat", {}).get("id", "")
        durasi = exp.get("tahunDurasi", {}).get("id", "")
        desc = exp.get("deskripsi", {}).get("id", "")
        lines.append(f"{eid}. {judul} - {tempat} ({durasi})")
        if desc: lines.append(f"   {desc}")
    lines.append("")

    # 7. kontak
    lines.append("=== KONTAK & KOLABORASI ===")
    lines.append(f"{profile.get('contactTitle', 'Hubungi saya.')} {profile.get('contactDesc', '')}")
    lines.append("Website: https://fathifadhil.me")
    lines.append(f"Email: {profile.get('email', '')}")
    lines.append(f"WhatsApp: {data.get('contact', {}).get('whatsappNumber', '')}")
    lines.append(f"GitHub: {profile.get('githubLink', '')}")
    lines.append(f"LinkedIn: {profile.get('linkedinLink', '')}")

    return "\n".join(lines)

_DYNAMIC_CONTEXT = _build_context_from_json()

PORTFOLIO_CONTEXT = _DYNAMIC_CONTEXT if _DYNAMIC_CONTEXT else """
=== PROFIL UTAMA ===
Nama: Fathi Fadhil
Website: fathifadhil.me
Fokus: Full Stack Developer, Flutter Developer, Creative Engineer, AI Explorer
Status: Available for Work & Freelance
Jurusan: Teknik Informatika
Email: fathifadhil10@gmail.com
LinkedIn: https://www.linkedin.com/in/fathi-fadhil-45063320a
GitHub: https://github.com/Fathii3
Instagram: https://instagram.com/fathii._3
CV: https://drive.google.com/file/d/19l2IONrbC1H53HT328mxmsAwhIJ9Cf35/view
WhatsApp: +6282241211466
Deskripsi: Suka eksplorasi teknologi web, mobile, dan AI untuk membangun aplikasi yang bermanfaat. Setiap proyek jadi tempat belajar dan berkembang.
Motivasi: "Inovasi membedakan seorang pemimpin dari seorang pengikut."

=== TECH STACK ===
Bahasa Pemrograman: JavaScript, TypeScript, Dart, Python, PHP, C++, HTML5, CSS3
Framework & Frontend: React, Next.js, Flutter, Tailwind CSS, Framer Motion, Vite
Backend & Database: Node.js, Express.js, PostgreSQL, MySQL, SQLite, Firebase, Supabase
DevOps & AI: Docker, Git, GitHub, Gemini AI, Streamlit

=== PROYEK UNGGULAN ===
1. FINARA (Agustus 2026) ★ Featured - Flutter, Dart, SQLite, Google Gemini AI API, POS & Personal Finance
2. SKM Langkat - Survei Kepuasan Masyarakat (Agustus 2026) ★ Featured - Laravel 13, PHP 8.3, Tailwind CSS v4, PKL
3. SiBanjir (Juni 2026) ★ Featured - Flutter, Dart, Firebase, Supabase, Riverpod
4. Dapur Ode (Juni 2026) ★ Featured - HTML, CSS, PHP, OpenRouteService
5. SecuScan (Juni 2026) ★ Featured - Flutter, Dart, Firestore, AES-256
6. Polynomial Field Calculator (Mei 2026) ★ Featured - Python3, Flask
7. Wi-Fi Connect & Network Monitoring System (Juli 2026) ★ Featured - Node.js, Tailwind, Puppeteer
8. fets - Platform Source Code & Template Web (Agustus 2026) ★ Featured - Tailwind, Firestore REST API
9. Dist - Hub Distribusi Berkas & APK Developer Modern (Agustus 2026) ★ Featured - Next.js 14, React 18
10. Fetty Assistant - Asisten Portofolio Interaktif Berbasis AI (September 2026) ★ Featured - Python, Streamlit, Gemini

=== SERTIFIKASI ===
1. #JuaraVibeCoding Participant - Google Developer Groups (Mei 2026)
2. IT - AI Agent for Programming - IBM SkillsBuild x Hacktiv8 Indonesia (Juli 2026)
3. Gemini Certified Student - Google for Education (Mei 2026 - Mei 2029)
4. HCIA-AI V4.0 Course - Huawei ICT Academy (Mei 2026)
5. HCIA-Datacom V1.0 Course - Huawei ICT Academy (Mei 2026)
6. Selected Delegate International Webinar - Yayasan Duta Inspirasi Indonesia (Agustus 2025)

=== PENGALAMAN ===
1. Praktik Kerja Lapangan (PKL) - Diskominfo Kabupaten Langkat (Juli - Agustus 2026)
2. Pengembangan Mandiri & Eksplorasi Teknologi (2025 - Sekarang)

=== KONTAK & KOLABORASI ===
Website: https://fathifadhil.me
Email: fathifadhil10@gmail.com
WhatsApp: +6282241211466
GitHub: https://github.com/Fathii3
LinkedIn: https://www.linkedin.com/in/fathi-fadhil-45063320a
"""

