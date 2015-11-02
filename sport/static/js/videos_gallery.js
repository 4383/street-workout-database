/**
 * Created by herve on 26/10/15.
 */


//---------------------
// Video gallery
//---------------------
var json_videos_data = JSON.parse(gallery_content);

/**
 * Listen display event on modalVideoViewer.
 * Get ID of clicked thumbnail and update modal content
 */
$('#modalVideoViewer').on('show.bs.modal', function (event) {
    updateVideoViewerContent(event.relatedTarget.id);
});

/**
 * Select the corresponding JSON entry (by index) and update modal content.
 * @param video_id The JSON entry index for the current video
 */
function updateVideoViewerContent(video_id) {
    var json_entry = json_videos_data.gallery[video_id];
    document.getElementById("modalVideoViewerTitle").innerHTML = json_entry.title;
    document.getElementById("modalVideoViewerDescription").innerHTML = json_entry.description;
    document.getElementById("modalVideoViewerVideo").width = json_entry.player_width;
    document.getElementById("modalVideoViewerVideo").height = json_entry.player_height;
    document.getElementById("modalVideoViewerVideo").src = json_entry.embedded_url;
    document.getElementById("modalVideoViewerOriginalLink").href = json_entry.origin_url;
    document.getElementById("modalVideoViewerOriginalLink").innerHTML = json_entry.origin_url;
}
