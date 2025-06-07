let projectFiles = [];
let isOnlineAI = true;  // Flag to toggle between online/offline AI

// Handle file input and load files into projectFiles
document.getElementById('fileInput').addEventListener('change', (e) => {
  const files = e.target.files;
  for (const file of files) {
    const reader = new FileReader();
    reader.onload = (e) => {
      projectFiles.push({
        name: file.name,
        code: e.target.result
      });
      displayOutput();
    };
    reader.readAsText(file);
  }
});

// Function to trigger refactoring of code using either online or offline AI
async function runAIRefactor() {
  for (let i = 0; i < projectFiles.length; i++) {
    const refactored = isOnlineAI ? 
      await realAIRefactor(projectFiles[i].code) : 
      await localAIRefactor(projectFiles[i].code);
    projectFiles[i].code = refactored;
    projectFiles[i].status = 'refactored';
  }
  displayOutput();
}

// Function for refactoring using OpenAI's GPT model (online)
async function realAIRefactor(code) {
  const response = await fetch('https://api.openai.com/v1/chat/completions', {
    method: 'POST',
    headers: {
      'Authorization': 'AIzaSyAvrxOyAVzPVcnzxuD0mjKVDyS2bNWfC10',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      model: 'gpt-4',
      messages: [
        { role: 'system', content: 'You are a senior developer.' },
        { role: 'user', content: 'Refactor and optimize this code:\\n\\n' + code }
      ]
    })
  });
  const data = await response.json();
  return data.choices[0].message.content.trim();
}

// Function for local AI refactoring (offline using WebLLM)
async function localAIRefactor(code) {
  const chat = await webllm.createChat();
  await chat.reload("Llama-3-8B-Instruct"); // Load Llama model
  const reply = await chat.generate("Refactor and optimize this code:\n" + code);
  return reply;
}

// Toggle between online and offline AI modes
function toggleAI() {
  isOnlineAI = !isOnlineAI;
  alert(isOnlineAI ? 'Switched to Online AI (GPT)' : 'Switched to Offline AI (WebLLM)');
}

// Display the output of the current project files
function displayOutput() {
  const output = document.getElementById('output');
  output.textContent = projectFiles.map(f => `// ${f.name}\n${f.code}\n`).join('\n\n');
}

// Function to download the refactored project as a ZIP file
function downloadProject() {
  const zip = new JSZip();
  projectFiles.forEach(file => {
    zip.file(file.name, file.code);
  });
  zip.generateAsync({ type: "blob" }).then(content => {
    const a = document.createElement('a');
    a.href = URL.createObjectURL(content);
    a.download = "refactored_project.zip";
    a.click();
  });
}

// Function to save the project files locally using localForage
function saveToLocal() {
  localforage.setItem('my_project_files', projectFiles).then(() => {
    alert('Saved locally!');
  });
}

// Function to load the project files from local storage
function loadFromLocalStorage() {
  localforage.getItem('my_project_files').then(data => {
    if (data) {
      projectFiles = data;
      displayOutput();
    } else {
      alert('No saved project found.');
    }
  });
}

async function runAIRefactor() {
  for (let i = 0; i < projectFiles.length; i++) {
    // Refactor code using AI
    const refactored = isOnlineAI ? 
      await realAIRefactor(projectFiles[i].code) : 
      await localAIRefactor(projectFiles[i].code);
    
    // Analyze code complexity
    const complexityReport = await analyzeCodeComplexity(refactored);
    console.log(`Complexity report for ${projectFiles[i].name}:`, complexityReport);

    // Generate documentation
    const documentation = await generateDocumentation(refactored);
    console.log(`Generated documentation for ${projectFiles[i].name}:`, documentation);

    // Format the code
    const formattedCode = await formatCode(refactored);
    console.log(`Formatted code for ${projectFiles[i].name}:`, formattedCode);

    // Generate unit tests
    const unitTests = await generateUnitTests(refactored);
    console.log(`Generated unit tests for ${projectFiles[i].name}:`, unitTests);

    // Add comments to code
    const commentedCode = await addCodeComments(formattedCode);
    console.log(`Commented code for ${projectFiles[i].name}:`, commentedCode);

    // Update the file with the final version
    projectFiles[i].code = commentedCode;
    projectFiles[i].status = 'refactored and commented';
  }
  displayOutput();
}

// Function to analyze code complexity and suggest improvements (AI-powered)
async function analyzeCodeComplexity(code) {
  const analysisPrompt = `Analyze the following code and provide a complexity report and suggestions for optimization. Code:\n\n${code}`;
  
  const response = await fetch('https://api.openai.com/v1/chat/completions', {
    method: 'POST',
    headers: {
      'Authorization': 'AIzaSyAvrxOyAVzPVcnzxuD0mjKVDyS2bNWfC10',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      model: 'gpt-4',
      messages: [
        { role: 'system', content: 'You are a software engineer specializing in code analysis.' },
        { role: 'user', content: analysisPrompt }
      ]
    })
  });
  const data = await response.json();
  return data.choices[0].message.content.trim();
}

// Function to generate documentation for code using AI
async function generateDocumentation(code) {
  const docPrompt = `Generate documentation for the following code:\n\n${code}`;
  
  const response = await fetch('https://api.openai.com/v1/chat/completions', {
    method: 'POST',
    headers: {
      'Authorization': 'AIzaSyAvrxOyAVzPVcnzxuD0mjKVDyS2bNWfC10',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      model: 'gpt-4',
      messages: [
        { role: 'system', content: 'You are an expert software documentation generator.' },
        { role: 'user', content: docPrompt }
      ]
    })
  });
  const data = await response.json();
  return data.choices[0].message.content.trim();
}

// Function to format code using AI
async function formatCode(code) {
  const formatPrompt = `Format the following code to meet standard style conventions:\n\n${code}`;
  
  const response = await fetch('https://api.openai.com/v1/chat/completions', {
    method: 'POST',
    headers: {
      'Authorization': 'AIzaSyAvrxOyAVzPVcnzxuD0mjKVDyS2bNWfC10',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      model: 'gpt-4',
      messages: [
        { role: 'system', content: 'You are an expert code formatter.' },
        { role: 'user', content: formatPrompt }
      ]
    })
  });
  const data = await response.json();
  return data.choices[0].message.content.trim();
}

// Function to generate unit tests for code
async function generateUnitTests(code) {
  const testPrompt = `Generate unit tests for the following code using the appropriate testing framework (e.g., Jest, Mocha):\n\n${code}`;
  
  const response = await fetch('https://api.openai.com/v1/chat/completions', {
    method: 'POST',
    headers: {
      'Authorization': 'AIzaSyAvrxOyAVzPVcnzxuD0mjKVDyS2bNWfC10',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      model: 'gpt-4',
      messages: [
        { role: 'system', content: 'You are a test generation AI.' },
        { role: 'user', content: testPrompt }
      ]
    })
  });
  const data = await response.json();
  return data.choices[0].message.content.trim();
}

// Function to add comments to code
async function addCodeComments(code) {
  const commentPrompt = `Add comments to the following code to explain each function, variable, and complex logic:\n\n${code}`;
  
  const response = await fetch('https://api.openai.com/v1/chat/completions', {
    method: 'POST',
    headers: {
      'Authorization': 'AIzaSyAvrxOyAVzPVcnzxuD0mjKVDyS2bNWfC10',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      model: 'gpt-4',
      messages: [
        { role: 'system', content: 'You are a code commenting AI.' },
        { role: 'user', content: commentPrompt }
      ]
    })
  });
  const data = await response.json();
  return data.choices[0].message.content.trim();
}
