window.onload = function(){
    var firstname = sessionStorage.getItem('firstname');
    if(firstname !== null) $('#id_first_name').val(firstname)
    var lastname = sessionStorage.getItem('lastname');
    if(lastname !== null) $('#id_last_name').val(lastname)
    var sex = sessionStorage.getItem('sex');
    if(sex !== null) $('#id_sex').val(sex)
    var dateofbirth = sessionStorage.getItem('dateofbirth');
    if(dateofbirth !== null) $('#id_date_of_birth').val(dateofbirth)
    var address = sessionStorage.getItem('address');
    if(address !== null) $('#id_address').val(address)
    var contact = sessionStorage.getItem('contact');
    if(contact !== null) $('#id_contact').val(contact)
    var kin = sessionStorage.getItem('kin');
    if(kin !== null) $('#id_next_of_kin').val(kin)
    var conditions = sessionStorage.getItem('conditions');
    if(conditions !== null) $('#id_conditions').val(conditions)
    var facility = sessionStorage.getItem('facility');
    if(facility !== null) $('#id_facility_registered_from').val(facility)
    var visitationdate = sessionStorage.getItem('visitationdate');
    if(visitationdate !== null) $('#id_vistation_date').val(visitationdate)
    var nextvisit = sessionStorage.getItem('nextvisit');
    if(nextvisit !== null) $('#id_next_visit').val(nextvisit)

}