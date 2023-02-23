$(document).on("click", "#add-to-wishlist-button", function (e) {
    e.preventDefault();
    $.ajax({
        type: "POST",
        url: '{% url "account:add_to_wishlist" 1 %}',
        data: {
            productid: $("#add-to-wishlist-button").val(),
            csrfmiddlewaretoken: "{{csrf_token}}",
            action: "post",
        },
        success: function (json) {
            if (json.status == "Added") {
                document.getElementById("add-to-wishlist-button").innerHTML = "Remove from wishlist";
            } else {
                document.getElementById("add-to-wishlist-button").innerHTML = "Add to wishlist";
            }
        },
        error: function (xhr, errmsg, err) {},
    });
});
