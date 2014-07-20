$(document).ready(function() {
            function block_form() {
                $("#loading").show();
                $('textarea').attr('disabled', 'disabled');
                $('input').attr('disabled', 'disabled');
            }

            function unblock_form() {
                $('#loading').hide();
                $('textarea').removeAttr('disabled');
                $('input').removeAttr('disabled');
                $('.errorlist').remove();
            }

            // prepare Options Object for plugin
            var options = {
                beforeSubmit: function(form, options) {
                    // return false to cancel submit
                    block_form();
                },
                success: function() {
                    unblock_form();
                    $("#form_ajax").show();
                    setTimeout(function() {
                        $("#form_ajax").hide();
                    }, 5000);
                },
                error:  function(resp) {
                    unblock_form();
                    $("#form_ajax_error").show();
                    // render errors in form fields
                    var errors = JSON.parse(resp.responseText);
                    for (error in errors) {
                        var id = '#id_' + error;
                        $(id).parent('p').prepend(errors[error]);
                    }
                    setTimeout(function() {
                        $("#form_ajax_error").hide();
                    }, 5000);
                }
            };

            $('#conditionForm').ajaxForm(options);
            $('#otherConditionForm').ajaxForm(options);
        });