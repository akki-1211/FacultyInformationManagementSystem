 // open create folder modal
 $('.js-upload-file-btn').on('click', function() {
     $(".js-upload-file, .modal-backdrop").addClass("open");
 });

 // close all modal
 $(document).on('click', '.modal .close', function() {
     $(".modal, .modal-backdrop").removeClass("open");

 });


 Dropzone.autoDiscover = false;
 try {
     var myDropzone = new Dropzone("#dropzone", {
         paramName: "file", // The name that will be used to transfer the file
         maxFilesize: .5, // MB

         addRemoveLinks: true,
         dictDefaultMessage: '<span class="bigger-150 bolder"><i class=" fa fa-caret-right red"></i> Drop files</span> to upload \
            <span class="smaller-80 grey">(or click)</span> <br /> \
            <i class="upload-icon fa fa-cloud-upload blue fa-3x"></i>',
         dictResponseError: 'Error while uploading file!',

         //change the previewTemplate to use Bootstrap progress bars

     });
 } catch (e) {
     //  alert('Dropzone.js does not support older browsers!');
 }