function addNewProduct(url) {
    // This function is responsible for adding a new product through the CRUDs API
    // Receives the urlProds, which is the URL for the API
    // returns nothing

    $.ajax({
        url: url,
        type: "POST",
        data: {
            "name": document.getElementById("prod_name_modal").value,
            "price": document.getElementById("prod_price_modal").value,
        },
        async: true,
        success: function (response) {
            console.log("addNewProduct", response);
            $('#productModal').modal('toggle');
            $('#prod_id_modal').val("");
            $('#prod_name_modal').val("");
            $('#prod_price_modal').val("");
            $("#btn-delete-prod").addClass("d-none");

            window.location.reload();
        },
        error: function (response) {
            console.error("addNewProduct", response);
            $('#productModal').modal('toggle');
        },
    });
}

function updateProduct(url) {
    // This function is responsible for updating an already existing product through the CRUDs API
    // Receives the urlProds, which is the URL for the API
    // returns nothing

    $.ajax({
        url: url,
        type: "PUT",
        data: {
            "name": document.getElementById("prod_name_modal").value,
            "price": document.getElementById("prod_price_modal").value,
        },
        async: true,
        success: function (response) {
            $('#prod_id_modal').val("");
            $('#prod_name_modal').val("");
            $('#prod_price_modal').val("");
            $("#btn-delete-prod").addClass("d-none");
            console.log("updateProduct", response);
            $('#productModal').modal('toggle');
            window.location.reload();
        },
        error: function (response) {
            $('#prod_id_modal').val("");
            $('#prod_name_modal').val("");
            $('#prod_price_modal').val("");
            $("#btn-delete-prod").addClass("d-none");
            console.error("updateProduct", response);
            $('#productModal').modal('toggle');
        },
    });
}

function modalProduct(urlProds, urlProd, prod_id) {
    // This function is responsible for choosing what/how process the request (add or update product) through the CRUDs API
    // Receives the "urlProds" and "urlProds", which are the URLs for the respective APIs. Receives the product ID (prod_id) in case of using the "urlProd" url.
    // returns nothing

    if (prod_id === "") {
        addNewProduct(urlProds);
    } else {
        $("#btn-delete-prod").removeClass("d-none");
        updateProduct(urlProd.replace("0", prod_id));
    }
}

function modalAddProduct() {
    // This function is responsible for cleaning the modal to not leave residual data
    // returns nothing

    $('#prod_id_modal').val("");
    $('#prod_name_modal').val("");
    $('#prod_price_modal').val("");
    $("#btn-delete-prod").addClass("d-none");
}

function loadProductModal(url, prod_id) {
    // This function loads the data of a product to the product's modal
    // Receives the url, which is the URL for the API; Receives the product ID (prod_id), to add itself to the modal form
    // returns nothing
    $.ajax({
        url: url,
        type: "GET",
        async: true,
        success: function (response) {
            console.log(response);
            $("#btn-delete-prod").removeClass("d-none");
            $("#prod_id_modal").val(prod_id);
            $("#prod_name_modal").val(response["data"][0]["name"]);
            $("#prod_price_modal").val(response["data"][0]["price"]);
            $('#productModal').modal('toggle');
        },
        error: function (response) {
            $("#btn-delete-prod").addClass("d-none");
            console.error(response);
        },
    });
}

function deleteProduct(url, prod_id) {
    // This function is responsible for deleting the product ID provided (prod_id)
    // Receives the url, which is the URL for the API; receives the product ID (prod_id) to send to the API
    // returns nothing

    $.ajax({
        url: url.replace("0", prod_id),
        type: "DELETE",
        async: true,
        success: function (response) {
            console.log("deleteProduct", response);
            $('#productModal').modal('hide');
            $("#btn-delete-prod").addClass("d-none");
            $("#prod_id_modal").val("");
            window.location.reload();
        },
        error: function (response) {
            console.error("deleteProduct", response);
            $('#productModal').modal('hide');
        },
    });
}

async function addNewSell(url, urlSellsDetails) {
    // This function is responsible for adding a new sell, creating its sells details before, through the CRUDs API
    // returns nothing

    let all_details = document.getElementsByClassName("sells_details");
    console.log("0", all_details);
    let vals = [];
    for (var i = 0; i < all_details.length; i++) {
        var temp = await addNewSellDetail(urlSellsDetails, all_details[i].value, all_details[i].id);
        console.log("0.5", temp);
        vals.push(temp);
    }

    $.when(null, vals).done(function () {
        let sells_details = "";
        console.log("1", vals);
        vals.forEach((item) => {
            sells_details += item + ",";
            console.log("2", sells_details);
        });
        sells_details.slice(0, sells_details.length - 1);
        console.log("3", sells_details);

        $.ajax({
            url: url,
            type: "POST",
            data: {
                "sells_details": sells_details,
            },
            async: true,
            success: function (response) {
                console.log("addNewSell", response);
                //window.location.reload();
            },
            error: function (response) {
                console.error("addNewSell", response);
                //window.location.reload();
            },
        });
    });
}

function getSellsDetailsFromSellID(url, sell_id) {
    $.ajax({
        url: url.replace("0", sell_id),
        type: "GET",
        async: true,
        success: function (response) {
            return response["data"][0];
        },
        error: function (response) {
            return response["success"];
        },
    });
}

function updateSell(urlUpdateSell, urlGetSell) {
    // This function is responsible for updating an already existing product through the CRUDs API
    // Receives the urlProds, which is the URL for the API
    // returns nothing

    let all_details = getSellsDetailsFromSellID(urlGetSell);
    console.log("0", all_details);
    let vals = [];
    for (var i = 0; i < all_details.length; i++) {
        var temp = await(urlSellsDetails, all_details[i].value, all_details[i].id);
        console.log("0.5", temp);
        vals.push(temp);
    }

    $.when(null, vals).done(function () {
        $.ajax({
            url: urlUpdateSell,
            type: "PUT",
            data: {
                "qty": document.getElementById("prod_name_modal").value,
                "price": document.getElementById("prod_price_modal").value,
            },
            async: true,
            success: function (response) {
                $('#sell_id_modal').val("");
                $("#btn-delete-sell").addClass("d-none");
                console.log("updateProduct", response);
                $('#sellModal').modal('toggle');
                window.location.reload();
            },
            error: function (response) {
                $('#prod_id_modal').val("");
                $('#prod_name_modal').val("");
                $('#prod_price_modal').val("");
                $("#btn-delete-prod").addClass("d-none");
                console.error("updateProduct", response);
                $('#productModal').modal('toggle');
            },
        });
    });
}

function modalAddSell() {
    // This function is responsible for cleaning the modal to not leave residual data
    // returns nothing

    let sells_details = document.getElementsByClassName("sells_details");
    for (let i = 0; i < sells_details.length; i++) {
        sells_details[i].value = "0.0";
    }
    $("#sell_id_modal").val("");
    $("#btn-delete-sell").addClass("d-none");
}

function loadSellModal(url, sell_id) {
    // This function loads the data of a sell to the sell's modal
    // Receives the url, which is the URL for the API; Receives the sell ID (sell_id), to add itself to the modal form
    // returns nothing
    $.ajax({
        url: url,
        type: "GET",
        async: true,
        success: function (response) {
            console.log(response);
            $("#btn-delete-sell").removeClass("d-none");
            $("#sell_id_modal").val(sell_id);
            let sells_details = document.getElementsByClassName("sells_details");
            for (let i = 0; i < sells_details.length; i++) {
                for (let u = 0; u < response["data"][0]["sells_details"].length; u++) {
                    console.log("TEST", sells_details[i].id, response["data"][0]["sells_details"][u]["prod_id"]);
                    if (parseInt(sells_details[i].id) === response["data"][0]["sells_details"][u]["prod_id"]) {
                        sells_details[i].value = response["data"][0]["sells_details"][u]["qty"];
                    }
                }
            }

            $('#sellModal').modal('toggle');
        },
        error: function (response) {
            $("#btn-delete-sell").addClass("d-none");
            $('#sellModal').modal('toggle');
            console.error(response);
        },
    });
}

function modalSell(urlSells, urlSell, urlSellsDetails, urlSellDetails, sell_id) {
    // This function is responsible for choosing what/how process the request (add or update sell) through the CRUDs API
    // Receives the "urlProds" and "urlProds", which are the URLs for the respective APIs. Receives the sell ID (sell_id) in case of using the "urlProd" url.
    // returns nothing

    if (sell_id === "") {
        addNewSell(urlSells, urlSellDetails);
    } else {
        $("#btn-delete-sell").removeClass("d-none");
        updateSell(urlSell.replace("0", sell_id));
    }
}

function deleteSell(url, sell_id) {
    // This function is responsible for deleting the sell ID provided (sell_id)
    // Receives the url, which is the URL for the API; receives the sell ID (sell_id) to send to the API
    // returns nothing

    $.ajax({
        url: url.replace("0", sell_id),
        type: "DELETE",
        async: true,
        success: function (response) {
            console.log("deleteSell", response);
            $('#sellModal').modal('hide');
            $("#btn-delete-sell").addClass("d-none");
            $("#sell_id_modal").val("");
            window.location.reload();
        },
        error: function (response) {
            console.error("deleteProduct", response);
            $('#sellModal').modal('hide');
        },
    });
}

function addNewSellDetail(url, qty, prod_id) {
    // This function is responsible for adding a new sell detail through the CRUDs API
    // returns the sell detail ID on success
    return new Promise((resolve, reject) => {
        $.ajax({
            url: url,
            type: "POST",
            data: {
                "qty": qty,
                "prod_id": prod_id,
            },
            success: function (response) {
                console.log("addNewSellDetail", response["sell_detail_id"]);
                resolve(response["sell_detail_id"]);
            },
            error: function (response) {
                console.error("addNewSellDetail", response);
                reject(response["success"]);
            },
        });
    });
}
