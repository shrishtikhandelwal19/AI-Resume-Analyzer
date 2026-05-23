const { execSync, spawn } = require('child_process');
const fs = require('fs');

function tryCommand(command) {
  try {
    console.log(`Running: ${command}`);
    execSync(command, { stdio: 'inherit' });
    return true;
  } catch (err) {
    console.warn(`Command failed: ${command}. Error: ${err.message}`);
    return false;
  }
}

// 1. Try installing streamlit and requirements
console.log("Checking and installing Python dependencies...");
let installed = false;
if (fs.existsSync('requirements.txt')) {
  installed = tryCommand("python3 -m pip install -r requirements.txt") || 
              tryCommand("python -m pip install -r requirements.txt") ||
              tryCommand("pip3 install -r requirements.txt") ||
              tryCommand("pip install -r requirements.txt");
} else {
  installed = tryCommand("python3 -m pip install streamlit") || 
              tryCommand("python -m pip install streamlit") ||
              tryCommand("pip3 install streamlit") ||
              tryCommand("pip install streamlit");
}

if (!installed) {
  console.warn("Could not execute pip install. Streamlit may already be installed or container runs in a custom environment. Attempting launch...");
}

// 2. Launch Streamlit on port 3000
const args = ["run", "app.py", "--server.port", "3000", "--server.address", "0.0.0.0"];
console.log("Launching Streamlit: streamlit " + args.join(" "));

let streamlitProcess;
try {
  streamlitProcess = spawn("streamlit", args, { stdio: 'inherit' });
} catch (e) {
  console.log("Direct run via 'streamlit' failed. Trying python3 -m streamlit...");
}

if (!streamlitProcess) {
  try {
    streamlitProcess = spawn("python3", ["-m", "streamlit", ...args], { stdio: 'inherit' });
  } catch (e) {
    try {
      streamlitProcess = spawn("python", ["-m", "streamlit", ...args], { stdio: 'inherit' });
    } catch (err) {
      console.error("FATAL: Failed to launch Streamlit process via any command syntax.", err);
      process.exit(1);
    }
  }
}

streamlitProcess.on('close', (code) => {
  console.log(`Streamlit process exited with code ${code}`);
  process.exit(code || 0);
});

streamlitProcess.on('error', (err) => {
  console.error("Streamlit process encountered an error:", err);
  // Try fallback in case spawning 'streamlit' directly threw error asynchronously
  try {
    console.log("Applying fallback launch with python3 -m streamlit...");
    const fallback = spawn("python3", ["-m", "streamlit", ...args], { stdio: 'inherit' });
    fallback.on('close', (code) => process.exit(code || 0));
  } catch (err2) {
    console.error("Fallback launch failed:", err2);
    process.exit(1);
  }
});
