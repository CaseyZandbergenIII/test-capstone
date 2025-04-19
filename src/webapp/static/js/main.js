function goTo(path) {
  window.location.href = `${path}`
}

// Get references to key DOM elements
const dropZone = document.getElementById("drop-zone"); // The area where users can drop or click to upload files
const fileInput = document.getElementById("file-upload"); // The hidden file input element
const fileList = document.getElementById("file-list"); // Displays selected file names

// When the user selects files using the file input
fileInput.addEventListener("change", handleFiles);

// Allow drag-over to work by preventing default browser behavior
dropZone.addEventListener("dragover", (e) => e.preventDefault());

// When files are dropped onto the drop zone
dropZone.addEventListener("drop", (e) => {
  e.preventDefault(); // Prevent the default drop behavior
  fileInput.files = e.dataTransfer.files; // Assign the dropped files to the hidden file input
  handleFiles(); // Handle the files like a normal selection
});

// Handles selected or dropped files
function handleFiles() {
  const files = fileInput.files; // Get selected files
  if (files.length === 0) return; // If no files, exit early

  // Display selected file names in the UI
  fileList.textContent = Array.from(files)
    .map((file) => file.name) // Get file name
    .join(", "); // Join into a string

  // Send files to the server
  uploadFiles(files);
}

// Upload files to the server using Fetch API
function uploadFiles(files) {
  const formData = new FormData(); // Create form data to hold the files

  // Add each file to the form data under the "files" key
  Array.from(files).forEach((file) => formData.append("files", file));

  // Send the files to the backend at /upload
  fetch("/upload", {
    method: "POST",
    body: formData,
  })
    .then((response) => {
      // If the server redirects, follow the redirect
      if (response.redirected) {
        window.location.href = response.url;
      } else {
        return response.json(); // Otherwise, parse the JSON response
      }
    })
    .then((data) => {
      // If there's a message from the server, show it
      if (data && data.message) {
        alert(data.message);
      }
      // Reset the file input and file list
      fileInput.value = "";
      fileList.textContent = "No files chosen";
    })
    .catch((error) => {
      // Log any errors to the console
      console.error("Error:", error);
    });
}
