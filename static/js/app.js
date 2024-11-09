document.addEventListener('DOMContentLoaded', function () {
    // Load the PDF page as an image
    fetch('/api/render_pdf')
        .then(response => response.json())
        .then(data => {
            document.getElementById('pdf-page').src = data.image_path;
        })
        .catch(error => console.error("Error loading PDF:", error));

    // Handle the annotation button click
    document.getElementById('annotate-btn').addEventListener('click', function () {
        const annotationData = {
            text: "This is a comment",
            position: { x: 100, y: 150 }  // Sample position on the page
        };

        fetch('/api/annotate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(annotationData)
        })
        .then(response => response.json())
        .then(data => {
            console.log("Annotation response:", data);
        })
        .catch(error => {
            console.error("Error:", error);
        });
    });

    // Handle the save button click
    document.getElementById('save-btn').addEventListener('click', function() {
        // Send annotation data to the server for saving
        fetch('/api/save_annotations', { 
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(annotations) 
        })
        .then(response => response.blob()) // Get the PDF blob from the response
        .then(blob => {
            // Create a blob URL for the downloaded PDF
            const url = window.URL.createObjectURL(blob);

            // Create a temporary link element to trigger the download
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', 'annotated.pdf'); 
            document.body.appendChild(link);

            // Trigger the download
            link.click();

            // Clean up: remove the link and revoke the blob URL
            document.body.removeChild(link);
            window.URL.revokeObjectURL(url); 
        })
        .catch(error => {
            console.error("Error saving annotations:", error);
            alert("Error saving annotations. Please check the console for details.");
        });
    });
});
