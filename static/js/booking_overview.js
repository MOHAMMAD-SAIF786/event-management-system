const bookingData = JSON.parse(
    sessionStorage.getItem("bookingData")
);
console.log("Booking Data");
console.log(bookingData);
console.log(bookingData.hall);
console.log(bookingData.rooms)

function hideAllCards() {

    document.getElementById("hallCard").style.display = "none";

    document.getElementById("roomCard").style.display = "none";

    document.getElementById("furnitureCard").style.display = "none";

    document.getElementById("stageCard").style.display = "none";

    document.getElementById("serviceCard").style.display = "none";

    document.getElementById("cateringCard").style.display = "none";

}

if (!bookingData) {

    alert("No booking data found.");

    window.location.href = "/";

}
// hideAllCards();

function loadHall() {

    if (!bookingData.hall) {

        return;

    }

    document.getElementById("hallCard").style.display = "block";

    document.getElementById("hallSection").innerHTML = `
        <div class="summary-row">

            <div class="summary-left">

                <h4>${bookingData.hall.name}</h4>

                <small>Hall Booking</small>

            </div>

            <div class="summary-price">

                ₹${bookingData.hall.price.toLocaleString("en-IN")}

            </div>

        </div>
    `;
}
function loadFurniture() {

    document.getElementById("furnitureCard").style.display = "block";

    let html = "";

    bookingData.furniture.forEach(item => {

        html += `

            <div class="summary-row">

                <div class="summary-left">

                    <h4>${item.name}</h4>

                    <small>

                        ${item.quantity} × ₹${item.price}

                    </small>

                </div>

                <div class="summary-price">

                    ₹${item.total.toLocaleString("en-IN")}

                </div>

            </div>

        `;

    });

    document.getElementById("furnitureSection").innerHTML = html;

}
function loadStage() {

    document.getElementById("stageCard").style.display = "block";

    if (!bookingData.stage) return;

    document.getElementById("stageSection").innerHTML = `

        <div class="summary-row">

            <div class="summary-left">

                <h4>${bookingData.stage.name}</h4>

            </div>

            <div class="summary-price">

                ₹${bookingData.stage.price.toLocaleString("en-IN")}

            </div>

        </div>

    `;

}
function loadRooms() {

    document.getElementById("roomCard").style.display = "block";

    console.log("loadRooms Called");
    console.log(bookingData.rooms);

    if (!bookingData.rooms || bookingData.rooms.length === 0) {

        document.getElementById("roomSection").innerHTML = `
            <p>No rooms selected.</p>
        `;

        document.getElementById("summaryRoomPrice").innerText = "₹0";

        return;
    }

    let html = "";
    let total = 0;

    bookingData.rooms.forEach(room => {

        total += room.total;

        html += `

        <div class="summary-row">

            <div class="summary-left">

                <h4>${room.name}</h4>

                <small>
                    ${room.quantity} × ₹${room.price.toLocaleString("en-IN")}
                </small>

            </div>

            <div class="summary-price">

                ₹${room.total.toLocaleString("en-IN")}

            </div>

        </div>

        `;

    });

    document.getElementById("roomSection").innerHTML = html;

    document.getElementById("summaryRoomPrice").innerText =
        "₹" + total.toLocaleString("en-IN");

}
function loadServices() {

    document.getElementById("serviceCard").style.display = "block";

    let html = "";
    let serviceTotal = 0;

    function renderCategory(title, services) {

        if (services.length === 0) return;

        html += `
            <div class="summary-category">

                <h3>${title}</h3>

            </div>
        `;

        services.forEach(service => {

            serviceTotal += service.price;

            html += `

                <div class="summary-row">

                    <div class="summary-left">

                        <h4>${service.name}</h4>

                    </div>

                    <div class="summary-price">

                        ₹${service.price.toLocaleString("en-IN")}

                    </div>

                </div>

            `;

        });

    }

    renderCategory(
        "DJ & Entertainment",
        bookingData.entertainment
    );

    renderCategory(
        "Photography & Videography",
        bookingData.photography
    );

    renderCategory(
        "Guest Services",
        bookingData.guestServices
    );

    document.getElementById("servicesSection").innerHTML = html;

    return serviceTotal;

}
function loadCatering() {

    document.getElementById("cateringCard").style.display = "block";

    console.log("loadCatering Called");

    console.log(bookingData.catering);

    console.log(document.getElementById("cateringSection"));

    if (!bookingData.catering) {

        document.getElementById("cateringSection").innerHTML = `
            <p>No catering selected.</p>
        `;

        document.getElementById("summaryCateringPrice").innerText = "₹0";

        return;
    }

    let groupedItems = {};

    (bookingData.catering.selectedItems || []).forEach(menu => {

        if (!groupedItems[menu.section]) {

            groupedItems[menu.section] = [];

        }

        groupedItems[menu.section].push(menu.item);

    });

    let menuHTML = "";

    for (let section in groupedItems) {

        menuHTML += `

            <div class="menu-section">

                <h5>👉🏿 ${section}</h5>

                <ul>

        `;

        groupedItems[section].forEach(item => {

            menuHTML += `
                <li>✓ ${item}</li>
            `;

        });

        menuHTML += `

                </ul>

            </div>

        `;

    }

    document.getElementById("cateringSection").innerHTML = `

        <div class="summary-row">

            <div class="summary-left">

                <h4>${bookingData.catering.name}</h4>

                <small>

                    ${bookingData.catering.guestCount} Guests × ₹${bookingData.catering.pricePerPlate.toLocaleString("en-IN")}/Plate

                </small>

                ${menuHTML}

            </div>

            <div class="summary-price">

                ₹${bookingData.catering.total.toLocaleString("en-IN")}

            </div>

        </div>

    `;

    document.getElementById("summaryCateringPrice").innerText =
        "₹" + bookingData.catering.total.toLocaleString("en-IN");

}
function updateSummary() {

    let hallPrice = bookingData.hall
        ? bookingData.hall.price
        : 0;

    let roomPrice = bookingData.roomTotal || 0;

    let cateringTotal = bookingData.cateringTotal || 0;

    let furniturePrice = bookingData.furnitureTotal || 0;

    let stagePrice = bookingData.stage
        ? bookingData.stage.price
        : 0;

    let servicePrice = 0;

    [
        ...bookingData.entertainment,
        ...bookingData.photography,
        ...bookingData.guestServices

    ].forEach(item => {

        servicePrice += item.price;

    });

    document.getElementById(
        "summaryHallPrice"
    ).innerText =
        "₹" + hallPrice.toLocaleString("en-IN");

    document.getElementById(
        "summaryRoomPrice"
    ).innerText =
        "₹" + roomPrice.toLocaleString("en-IN");
    document.getElementById(
        "summaryCateringPrice"
    ).innerText =
        "₹" + cateringTotal.toLocaleString("en-IN");

    document.getElementById(
        "summaryFurniturePrice"
    ).innerText =
        "₹" + furniturePrice.toLocaleString("en-IN");

    document.getElementById(
        "summaryStagePrice"
    ).innerText =
        "₹" + stagePrice.toLocaleString("en-IN");

    document.getElementById(
        "summaryServicePrice"
    ).innerText =
        "₹" + servicePrice.toLocaleString("en-IN");

    let grandTotal =
        hallPrice +
        roomPrice +
        cateringTotal +
        furniturePrice +
        stagePrice +
        servicePrice;

    document.getElementById(
        "grandTotal"
    ).innerText =
        "₹" + grandTotal.toLocaleString("en-IN");

}
function getCookie(name) {

    let cookieValue = null;

    if (document.cookie && document.cookie !== "") {

        const cookies = document.cookie.split(";");

        for (let cookie of cookies) {

            cookie = cookie.trim();

            if (cookie.startsWith(name + "=")) {

                cookieValue =
                    decodeURIComponent(
                        cookie.substring(name.length + 1)
                    );

                break;

            }

        }

    }

    return cookieValue;

}
function modifyBooking() {

    window.history.back();

}
function confirmBooking() {

    const customer = {

        name:
            document.getElementById("customerName").value,

        phone:
            document.getElementById("customerPhone").value,

        email:
            document.getElementById("customerEmail").value,

        event_date:
            document.getElementById("eventDate").value,

        event_type:
            document.getElementById("eventType").value,

        special_request:
            document.getElementById("specialRequest").value

    };

    if (
        customer.name === "" ||
        customer.phone === "" ||
        customer.event_date === "" ||
        customer.event_type === ""

    ) {

        alert("Please fill all required fields.");

        return;

    }

    bookingData.customer = customer;

    console.log(bookingData);

    bookingData.customer = customer;

    fetch("/booking/create/", {

        method: "POST",

        headers: {

            "Content-Type": "application/json",

            "X-CSRFToken": getCookie("csrftoken")

        },

        body: JSON.stringify(bookingData)

    })

        .then(response => response.json())

        .then(data => {

            console.log(data);

            if (data.status === "success") {

                window.location.href =
                    `/booking/${data.booking_id}/quotation/`;

            }
            else {

                alert(data.message);

            }

        })

        .catch(error => {

            console.log(error);

        });

}


hideAllCards();

if (bookingData.hall) {
    loadHall();
}

if (bookingData.rooms && bookingData.rooms.length > 0) {
    loadRooms();
}

if (bookingData.furniture && bookingData.furniture.length > 0) {
    loadFurniture();
}

if (bookingData.stage) {
    loadStage();
}

if (
    (bookingData.entertainment && bookingData.entertainment.length > 0) ||
    (bookingData.photography && bookingData.photography.length > 0) ||
    (bookingData.guestServices && bookingData.guestServices.length > 0)
) {
    loadServices();
}

if (bookingData.catering) {
    loadCatering();
}

updateSummary();