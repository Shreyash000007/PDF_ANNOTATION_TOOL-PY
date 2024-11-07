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
});
