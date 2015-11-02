$(document).scroll(function() {
    $('#sticky-main-menu').css({display: $(this).scrollTop()>100 ? "block":"none"});
});

//-------------------
// How-to
//-------------------
$(".show-step-description").click(function(event){
    var id = event.target.id.substr(event.target.id.length - 1);
    var class_type = "glyphicon glyphicon-resize-small";
    console.log("#collapseDescription" + id);
    console.log($("#collapseDescription" + id).attr("class"));
    if ("collapse in" == $("#collapseDescription" + id).attr("class")) {
        class_type = "glyphicon glyphicon-resize-full";
    }
    $("#collapseStepBtnSpan" + id).attr("class", class_type);
});

//-------------------
// Grid / List
//-------------------
$('#show-list').click(function() {
    document.getElementById("exercises-grid").className = "hidden";
    document.getElementById("exercises-list").className = "visible";
    document.getElementById("show-list").className = "btn btn-primary btn-lg";
    document.getElementById("show-grid").className = "btn btn-default btn-lg";
});
$('#show-grid').click(function() {
    document.getElementById("exercises-grid").className = "visible";
    document.getElementById("exercises-list").className = "hidden";
    document.getElementById("show-list").className = "btn btn-default btn-lg";
    document.getElementById("show-grid").className = "btn btn-primary btn-lg";
});
$('#level-all').click(function() {
    $('.easy').css('display', 'block');
    $('.medium').css('display', 'block');
    $('.hard').css('display', 'block');
});
$('#level-easy').click(function() {
    $('.easy').css('display', 'block');
    $('.medium').css('display', 'none');
    $('.hard').css('display', 'none');
});
$('#level-medium').click(function() {
    $('.easy').css('display', 'none');
    $('.medium').css('display', 'block');
    $('.hard').css('display', 'none');
});
$('#level-hard').click(function() {
    $('.easy').css('display', 'none');
    $('.medium').css('display', 'none');
    $('.hard').css('display', 'block');
});


//----------------------
// Muscle mapping
//----------------------
var json_images_data = JSON.parse(gallery_content);
var reverse_json_images_data = JSON.parse(reverse_gallery_content);

var MappingManager = MappingManager || {};
MappingManager.Mapping = function() {

    var overArea = function(area_id) {
        console.log("areahover");
        console.log(area_id);
        image = json_images_data[area_id]['image2'];
        muscle_link = json_images_data[area_id]['muscle'] + '_link';
        document.getElementById(area_id + "_img").src = image;
        document.getElementById(muscle_link).className = "btn btn-xs btn-danger";
    };

    var outArea = function(area_id) {
        console.log(area_id);
        image = json_images_data[area_id]['image1'];
        muscle_link = json_images_data[area_id]['muscle'] + '_link';
        document.getElementById(area_id + "_img").src = image;
        document.getElementById(muscle_link).className = "btn btn-xs btn-success";
    };

    var btnHover = function(muscle_id) {
        console.log("btnhover");
        image = reverse_json_images_data[muscle_id]['image2'];
        area_link = reverse_json_images_data[muscle_id]['area'] + '_img';
        document.getElementById(area_link).src = image;
        document.getElementById(muscle_id + "_link").className = "btn btn-xs btn-danger";
    }

    var btnOut = function(muscle_id) {
        image = reverse_json_images_data[muscle_id]['image1'];
        area_link = reverse_json_images_data[muscle_id]['area'] + '_img';
        document.getElementById(area_link).src = image;
        document.getElementById(muscle_id + "_link").className = "btn btn-xs btn-success";
    }

    var oPublic = {
        overArea: overArea,
        outArea: outArea,
        btnHover: btnHover,
        btnOut: btnOut
    }

    return oPublic;
}();

$('.mapping_area').mouseover(function (event) {
    area_id = event.target.id;
    MappingManager.Mapping.overArea(area_id);
});

$('.mapping_area').mouseout(function (event) {
    area_id = event.target.id;
    MappingManager.Mapping.outArea(area_id);
});

$('.muscle-link').mouseover(function (event) {
    btn_id = event.target.id;
    btn_id = btn_id.replace("_link", "");
    MappingManager.Mapping.btnHover(btn_id);
});
$('.muscle-link').mouseout(function (event) {
    btn_id = event.target.id;
    btn_id = btn_id.replace("_link", "");
    MappingManager.Mapping.btnOut(btn_id);
});