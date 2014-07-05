$('#closeButton').click( function(e){
        restoreItems();
        console.log('this was called')
    });

    function restoreItems(){
        window.onbeforeunload = function(){
        sessionStorage.setItem('firstname', $('#id_first_name').val());
        sessionStorage.setItem('lastname', $('#id_last_name').val());
        sessionStorage.setItem('sex', $('#id_sex').val());
        sessionStorage.setItem('dateofbirth', $('#id_date_of_birth').val());
        sessionStorage.setItem('address', $('#id_address').val());
        sessionStorage.setItem('contact', $('#id_contact').val());
        sessionStorage.setItem('kin', $('#id_next_of_kin').val());
        sessionStorage.setItem('conditions', $('#id_conditions').val());
        sessionStorage.setItem('facility', $('#id_facility_registered_from').val());
        sessionStorage.setItem('visitationdate', $('#id_vistation_date').val());
        sessionStorage.setItem('nextvisit', $('#id_next_visit').val());

    };

    window.location.href=window.location.href;
    console.log('this was called + 1')
}
