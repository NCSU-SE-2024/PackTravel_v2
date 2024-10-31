## Installation and Setup Instructions

### Prerequisite:
  - Download [Python3.10](https://www.python.org/downloads/).
  - Download [Django](https://docs.djangoproject.com/en/4.1/topics/install/).

Create a virtual environment:

```bash
  python3.x -m venv env
```

Activate the virtual environment:
Linux/MacOS:
```bash
  source env/bin/activate
```
Windows:
```bash
  ./env/Scripts/activate
```

Clone the project

```bash
  git clone https://github.com/KoruptTinker/PackTravel.git
```

Go to the project directory

```bash
  cd PackTravel
```

Install dependencies

```bash 
  pip install -r requirements.txt
```

# Google Cloud Setup for Google Maps Integration

## **1. Create a Google Cloud Account and Get an API Key for Google Maps Integration**

### Step 1: Sign Up for Google Cloud
1. Visit the [Google Cloud Console](https://console.cloud.google.com/).
2. If you don't have a Google Cloud account, sign up by following the on-screen instructions.
3. You may be required to enter billing information. Google Cloud offers $300 in free credits for new users.

### Step 2: Create a New Project
1. Once logged in, click on the **Select a project** dropdown at the top of the page.
2. Click **New Project**.
3. Enter a name for your project and select your billing account if prompted.
4. Click **Create**.

### Step 3: Enable the Google Maps API
1. In the left-hand menu, navigate to **APIs & Services** > **Library**.
2. In the search bar, type "Google Maps" and select the appropriate API (*Maps JavaScript API*).
3. Click **Enable** to activate the API for your project.

### Step 4: Get Your API Key
1. Go to **APIs & Services** > **Credentials** from the left-hand menu.
2. Click **Create Credentials** at the top of the page and select **API Key**.
3. A new API key will be generated. Copy this key as you'll need it to integrate Google Maps into your application.

### Step 5: Restrict Your API Key (Optional but Recommended)
1. In the **Credentials** tab, find your newly created API key and click on its name.
2. Under **Key restrictions**, you can limit usage by:
   - HTTP referrers (websites)
   - IP addresses (servers or devices)
   - Apps (Android or iOS)
3. Under **API restrictions**, you can restrict which APIs this key can access (only enable *Maps JavaScript API*).
4. Click **Save** after making any changes.

---

## **2. Create a Service Account and Get Its `credentials.json`**

### Step 1: Create a Service Account
1. In the Google Cloud Console, navigate to **IAM & Admin** > **Service Accounts** from the left-hand menu.
2. Click **+ CREATE SERVICE ACCOUNT** at the top of the page.
3. Enter a name for your service account and an optional description.
4. Click **Create and Continue**.

### Step 2: Assign Roles to Your Service Account
1. On the next screen, assign roles to your service account based on what permissions it needs (e.g., *Editor*, *Viewer*, etc.).
2. Click **Continue** after selecting roles.
3. You can skip granting users access to this service account, then click **Done**.

### Step 3: Generate `credentials.json`
1. After creating your service account, find it in the list under **IAM & Admin** > **Service Accounts**.
2. Click on your service account's name, then go to the **Keys** tab.
3. Click **Add Key**, then select **Create New Key**.
4. Choose JSON as the key type and click **Create**.
5. A `credentials.json` file will be downloaded automatically to your computer.

### Step 4: Secure Your `credentials.json`
- Store this file securely as it contains sensitive information that allows access to your Google Cloud resources.
- Use this file in your application when authenticating with Google Cloud services.

---

Make sure to keep both your API key and `credentials.json` secure!


### Copy `.devenv` to `.env`
1. Open your terminal or command prompt.
2. Run the following command to copy the `.devenv` file to `.env`:

   ```bash
   cp .devenv .env
3. Add appropriate API keys and MongoDB Connection URL to the env.
4. Start the server

```bash
  python manage.py migrate
  python manage.py runserver
```

     - Site gets hosted at:
       `http://127.0.0.1:8000/`
