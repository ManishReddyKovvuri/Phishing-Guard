# 🛡️ PhishingGuard

## 🌐 Website

Visit the [official website](https://soft-speculoos-81d235.netlify.app/) for more information.

**PhishingGuard** is an advanced tool designed to detect phishing or scam links in emails. With the increasing prevalence of email-based cyber threats, PhishingGuard provides a robust solution to help users stay safe online by analyzing email content and identifying malicious links before they cause harm.

---

## ✨ Features

- **Real-Time Phishing Detection:** Analyzes email links and content to detect potential threats.
- **User-Friendly Interface:** Simple and intuitive design for easy navigation.
- **Fast and Efficient:** Quickly scans email links to provide immediate feedback.
- **Cloud-Based Solution:** No need for software installation, accessible from any device.
- **Privacy-Focused:** Does not store user data, ensuring security and confidentiality.

---

## 📧 Contact

For any queries or suggestions, reach out via:
- Email: [phishingguard.help@icloud.com](mailto:phishingguard.help@icloud.com)

---

## 🧱 System Architecture

```mermaid
flowchart TD
    %% Core Processing Components
    subgraph "Core Processing"
        EI("Email Intake (mail.py)"):::core
        UE("URL Extraction (GetUrls.py)"):::core
        PDE("Phishing Detection Engine (detection.py)"):::core
        ML("ML Model (model.pkl)"):::data
        EI -->|"processes"| UE
        UE -->|"extracts"| PDE
        PDE -->|"loads"| ML
    end

    %% Helper Modules Group
    subgraph "Helper Modules"
        API("API Authentication Helper"):::helper
        SSL("SSL Certificate Helper"):::helper
        LOG("Logging Utility"):::helper
        MU("Models Utility"):::helper
        SEL("Selenium-based URL Redirection Helper"):::helper
        UH("URL Helper Functions"):::helper
    end

    %% Relationships between Detection Engine and Helpers
    PDE -->|"calls"| API
    PDE -->|"verifies"| SSL
    PDE -->|"logs_via"| LOG
    PDE -->|"invokes"| MU
    PDE -->|"handles_redirects"| SEL
    PDE -->|"validates"| UH

    %% Click Events
    click EI "https://github.com/manishreddykovvuri/phishing-guard/blob/main/mail.py"
    click UE "https://github.com/manishreddykovvuri/phishing-guard/blob/main/GetUrls.py"
    click PDE "https://github.com/manishreddykovvuri/phishing-guard/blob/main/detection.py"
    click ML "https://github.com/manishreddykovvuri/phishing-guard/blob/main/data/model.pkl"
    click API "https://github.com/manishreddykovvuri/phishing-guard/blob/main/helpers/api_auth.py"
    click SSL "https://github.com/manishreddykovvuri/phishing-guard/blob/main/helpers/get_ssl_certificate.py"
    click LOG "https://github.com/manishreddykovvuri/phishing-guard/blob/main/helpers/logger.py"
    click MU "https://github.com/manishreddykovvuri/phishing-guard/blob/main/helpers/models.py"
    click SEL "https://github.com/manishreddykovvuri/phishing-guard/blob/main/helpers/selenium_redirected_url.py"
    click UH "https://github.com/manishreddykovvuri/phishing-guard/blob/main/helpers/url_helper.py"

    %% Styling Classes
    classDef core fill:#FAD7A0,stroke:#E67E22,stroke-width:2px;
    classDef helper fill:#AED6F1,stroke:#3498DB,stroke-width:2px;
    classDef data fill:#A9DFBF,stroke:#27AE60,stroke-width:2px;
