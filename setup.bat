@echo off
setlocal enabledelayedexpansion

:: Function to check if a command exists
:checkCommand
where /q %1 >nul 2>&1
if %errorlevel% neq 0 (
    set "%2=0"
) else (
    set "%2=1"
)
exit /b 0

:: Function to download and install an application
:downloadAndInstall
echo Downloading and installing %1...
powershell -Command "Start-Process msiexec.exe -ArgumentList '/i %2 /quiet' -NoNewWindow -Wait"
if %errorlevel% neq 0 (
    echo Error: Failed to install %1. Exiting script.
    exit /b 1
)
exit /b 0

:: Step 0: Check and install Git
echo Checking Git installation...
call :checkCommand git gitInstalled
if !gitInstalled! equ 1 (
    call :downloadAndInstall Git "https://github.com/git-for-windows/git/releases/download/v2.42.0.windows.1/Git-2.42.0-64-bit.exe"
)

:: Step 1: Check and install Docker
echo Checking Docker installation...
call :checkCommand docker dockerInstalled
if !dockerInstalled! equ 1 (
    call :downloadAndInstall Docker "https://desktop.docker.com/win/stable/Docker%20Desktop%20Installer.exe"
)

:: Step 2: Check and install Docker Compose
echo Checking Docker Compose installation...
docker compose version >nul 2>&1
if %errorlevel% neq 0 (
    echo Docker Compose not found, installing...
    powershell -Command "Invoke-WebRequest -Uri https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-Windows-x86_64.exe -OutFile %ProgramFiles%\Docker\Docker\resources\bin\docker-compose.exe"
)

:: Step 3: Check and install Node.js and npm
echo Checking Node.js installation...
call :checkCommand node nodeInstalled
if !nodeInstalled! equ 1 (
    call :downloadAndInstall Node.js "https://nodejs.org/dist/v18.17.0/node-v18.17.0-x64.msi"
)

:: Step 4: Check and install Supabase CLI
echo Checking Supabase CLI installation...
call :checkCommand supabase supabaseInstalled
if !supabaseInstalled! equ 1 (
    echo Installing Supabase CLI...
    npm install -g supabase || (
        echo Error: Failed to install Supabase CLI.
        exit /b 1
    )
)

:: Step 5: Clone the repository
echo Cloning Quivr repository...
git clone https://github.com/quivrhq/quivr.git || (
    echo Error: Failed to clone repository.
    exit /b 1
)
cd quivr || exit /b 1

:: Step 6: Copy the .env.example to .env
echo Copying environment file...
copy .env.example .env || (
    echo Error: Failed to copy .env file.
    exit /b 1
)

:: Step 7: Update the .env file with OPENAI_API_KEY
set /p OPENAI_API_KEY="Enter your OPENAI_API_KEY: "
powershell -Command "(Get-Content .env) -replace 'OPENAI_API_KEY=.*', 'OPENAI_API_KEY=%OPENAI_API_KEY%' | Set-Content .env"

:: Step 8: Start the Supabase services
echo Starting Supabase services...
cd backend && supabase start || (
    echo Error: Failed to start Supabase.
    exit /b 1
)
cd ..

:: Step 9: Pull and start Docker containers
echo Pulling and starting Docker containers...
docker compose pull || (
    echo Error: Failed to pull Docker containers.
    exit /b 1
)
docker compose up || (
    echo Error: Failed to start Docker containers.
    exit /b 1
)

:: Step 10: Instructions to access the app
echo Setup complete. You can now access the Quivr app at http://localhost:3000/login with the credentials admin@quivr.app & admin.
pause

endlocal
