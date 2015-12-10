/**
 * Created by herve on 26/10/15.
 */
//---------------------
// Image Gallery
//---------------------
var json_images_data = JSON.parse(gallery_content);

/**
 * Listen display event on modalImageViewer.
 * Get ID of clicked thumbnail and update modal content
 */
$('#modalImageViewer').on('show.bs.modal', function (event) {
    updateImageViewerContent(event.relatedTarget.id);
});

/**
 * Select the corresponding JSON entry (by index) and update modal content.
 * @param image_id The JSON entry index for the current image
 */
function updateImageViewerContent(image_id) {
    var json_entry = json_images_data.gallery[image_id];
    document.getElementById("modalImageViewerTitle").innerHTML = json_entry.title;
    document.getElementById("modalImageViewerDescription").innerHTML = json_entry.description;
    document.getElementById("modalImageViewerImage").alt = json_entry.alt;
    document.getElementById("modalImageViewerImage").src = json_entry.image;
}
