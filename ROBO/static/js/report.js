async function getitems() {
    const response = await fetch(`/getitems/`);
    let data = await response.json();
    return data;
};
let itemData;
getitems().then(d => {
    itemData = JSON.parse(d);
}).catch(e => {
    console.log(e);
});
let choice = document.getElementById("Choice");
let reportDate = document.getElementById("reportDate");
let reportMonth = document.getElementById("reportMonth");
let reportYear = document.getElementById("reportYear");
reportDate.style.display = "block";
choice.addEventListener("change", () => {
    if (choice.value == "dailyReport") {
        reportDate.style.display = "block";
        reportMonth.style.display = "none";
        reportYear.style.display = "none";
    }
    else if (choice.value == "monthlyReport") {
        if (reportYear.style.gridColumnStart == "1" && reportYear.style.gridColumnEnd == "3") {
            reportYear.style.gridColumnStart = "auto";
            reportYear.style.gridColumnEnd = "auto";
        }
        reportDate.style.display = "none";
        reportMonth.style.display = "block";
        reportYear.style.display = "block";
    }
    else {
        reportDate.style.display = "none";
        reportMonth.style.display = "none";
        reportYear.style.display = "block";
        reportYear.style.gridColumnStart = "1";
        reportYear.style.gridColumnEnd = "3";
    }
});
let submitbtn = document.getElementById("submitbtn");
let reportGrid = document.getElementById("reportGrid");
let actualReport = document.getElementById("actualReport");
let dateSelected = document.querySelector("#reportDate > input");
let monthSelected = document.querySelector("#reportMonth > select");
let yearSelected = document.querySelector("#reportYear > input");
let reportSection = document.getElementById("reportSection");
let pageHeading = document.querySelector("#reportSection > div");
let html = "";
let orderHtml = "";
let maintanaceHtml = "";
submitbtn.addEventListener("click", () => {
    if (window.innerWidth > 1000) {
        let todayDate = new Date();
        if (choice.value == "dailyReport") {
            let dateSelectedObj = new Date(dateSelected.value);
            if (dateSelectedObj == "Invalid Date" || dateSelectedObj.getFullYear() > todayDate.getFullYear()) {
                alert("Invalid Date");
            } else {
                pageHeading.innerHTML = "DAILY REPORT";
                reportGrid.style.display = "none";
                actualReport.style.display = "grid";
                reportSection.style.margin = "1.5rem 5rem";
                let date = "";
                let month = "";
                if (dateSelectedObj.getDate() < 10) {
                    date = `0${dateSelectedObj.getDate()}`;
                }
                else {
                    date = dateSelectedObj.getDate();
                }
                if (dateSelectedObj.getMonth() + 1 < 10) {
                    month = `0${dateSelectedObj.getMonth() + 1}`;
                } else {
                    month = dateSelectedObj.getMonth() + 1;
                }
                async function getOrders() {
                    const response = await fetch(`/getOrders/${date}${month}${dateSelectedObj.getFullYear()}/`);
                    let data = await response.json();
                    return data;
                };
                async function getMaintenances() {
                    const response = await fetch(`/getMaintenances/${date}${month}${dateSelectedObj.getFullYear()}/`);
                    let data = await response.json();
                    return data;
                };
                let srNo = 1;
                let srNoMaintenance = 1;
                let orderCount = 0;
                let cash = 0;
                let online = 0;
                let maintenance = 0;
                let total = 0;
                getOrders().then(data => {
                    let orderData = JSON.parse(data);
                    html += `<div id="dailyReportdate">Date = ${date}/${month}/${dateSelectedObj.getFullYear()}</div>
                            <div id="Profit">
                                <div id="cashTotalDiv">
                                    <div id="cashTotal"></div>
                                </div>
                                <div id="onlineTotalDiv">
                                    <div id="onlineTotal"></div>
                                </div>
                                <div id="profitTotalDiv">
                                    <div id="profitTotal"></div>
                                </div>
                                <div id="backbtnContainer">
                                    <button id="btnBack">
                                        <svg class="btnsvg" viewBox="0 0 100 100" width="1rem">
                                            <line class="line top" x1="10" x2="50" y1="70" y2="50" stroke="black" stroke-width="10" stroke-linecap="round"></line>
                                            <line class="line bottom" x1="10" x2="100" y1="70" y2="70" stroke="black" stroke-width="10" stroke-linecap="round"></line>
                                            <line class="line bottom" x1="10" x2="50" y1="70" y2="90" stroke="black" stroke-width="10" stroke-linecap="round"></line>
                                        </svg>
                                        <div>Back</div>
                                    </button>
                                </div>
                            </div>`;
                    orderHtml += `<div id="orderReport">
                            <div>
                                <div class="tableHeading borderTopLeft">Sr No</div>
                                <div class="tableHeading">Table No.</div>
                                <div class="tableHeading">Pay Type</div>
                                <div class="tableHeading borderTopRight noBorderRight">Amount</div>
                            </div>`;
                    if (orderData.allOrders.length == 0) {
                        orderHtml += `<div>
                                        <div class="paddingItems borderLeft borderRight" id="noDataOrder">No Records To Show</div>
                                    </div>`;
                    } else {
                        orderData.allOrders.forEach(element => {
                            let parsedQuantity = JSON.parse(element.quantity_items);
                            let titleItems = "";
                            Object.entries(parsedQuantity).forEach(item => {
                                let [key, value] = item;
                                let keyIndex = itemData.item_id.indexOf(parseInt(key));
                                titleItems += `${itemData.name[keyIndex]} ${itemData.item_size[keyIndex]} [${value}] `;
                            });
                            if (orderData.allOrders.length == srNo) {
                                orderHtml += `<div title="${titleItems}">
                                        <div class="paddingItems borderLeft borderRight">${srNo}</div>
                                        <div class="paddingItems borderRight">${element.name}</div>
                                        <div class="paddingItems borderRight">${element.payment_type}</div>
                                        <div class="paddingItems borderRight">${element.total}</div>
                                    </div>`;
                            } else {
                                orderHtml += `<div class="borderBottom" title="${titleItems}">
                                        <div class="paddingItems borderLeft borderRight">${srNo}</div>
                                        <div class="paddingItems borderRight">${element.name}</div>
                                        <div class="paddingItems borderRight">${element.payment_type}</div>
                                        <div class="paddingItems borderRight">${element.total}</div>
                                    </div>`;
                            }
                            if (element.payment_type == "Cash") {
                                cash += element.total;
                                total += element.total;
                            }
                            if (element.payment_type == "Online") {
                                online += element.total;
                                total += element.total;
                            }
                            orderCount++;
                            srNo++;
                        });
                    }
                    orderHtml += `<div>
                            <div class="tableHeading borderBottomLeft" id="totalBlockOrder">Total</div>
                            <div class="tableHeading borderBottomRight noBorderRight">${total}</div>
                        </div>
                        </div>`;
                    getMaintenances().then(data => {
                        let maintenaceData = JSON.parse(data);
                        maintanaceHtml += `<div id="maintenanceReport">
                                        <div>
                                            <div class="tableHeading borderTopLeft">Sr No</div>
                                            <div class="tableHeading">Maintenance</div>
                                            <div class="tableHeading borderTopRight noBorderRight">Amount</div>
                                        </div>`;
                        if (maintenaceData.allMaintenance.length == 0) {
                            maintanaceHtml += `<div>
                                                <div class="paddingItems borderLeft borderRight" id="noDataMaintenance">No Records To Show</div>
                                            </div>`;
                        } else {
                            maintenaceData.allMaintenance.forEach(element => {
                                if (maintenaceData.allMaintenance.length == srNoMaintenance) {
                                    maintanaceHtml += `<div>
                                                        <div class="paddingItems borderLeft borderRight">${srNoMaintenance}</div>
                                                        <div class="paddingItems borderRight">${element.name}</div>
                                                        <div class="paddingItems borderRight">${element.price}</div>
                                                    </div>`;
                                } else {
                                    maintanaceHtml += `<div class="borderBottom">
                                                        <div class="paddingItems borderLeft borderRight">${srNoMaintenance}</div>
                                                        <div class="paddingItems borderRight">${element.name}</div>
                                                        <div class="paddingItems borderRight">${element.price}</div>
                                                    </div>`;
                                }
                                maintenance += element.price;
                                srNoMaintenance++;
                            });
                        }
                        maintanaceHtml += `<div>
                                            <div class="tableHeading borderBottomLeft" id="totalBlockMaintenance">Total</div>
                                            <div class="tableHeading borderBottomRight noBorderRight">${maintenance}</div>
                                        </div>
                                        </div>`;
                        html += orderHtml;
                        html += maintanaceHtml;
                        actualReport.innerHTML += html;
                        let cashTotal = document.getElementById("cashTotal");
                        cashTotal.innerHTML = `Cash = ${cash}`;
                        let onlineTotal = document.getElementById("onlineTotal");
                        onlineTotal.innerHTML = `Online = ${online}`;
                        let profitTotal = document.getElementById("profitTotal");
                        profitTotal.innerHTML = `Profit = ${total - maintenance}`;
                        let noDataOrder = document.getElementById("noDataOrder");
                        if (noDataOrder != null) {
                            noDataOrder.style.gridColumnStart = "1";
                            noDataOrder.style.gridColumnEnd = "5";
                            noDataOrder.style.textAlign = "center";
                        }
                        let noDataMaintenance = document.getElementById("noDataMaintenance");
                        if (noDataMaintenance != null) {
                            noDataMaintenance.style.gridColumnStart = "1";
                            noDataMaintenance.style.gridColumnEnd = "4";
                            noDataMaintenance.style.textAlign = "center";
                        }
                        let totalBlockOrder = document.getElementById("totalBlockOrder");
                        totalBlockOrder.style.gridColumnStart = "1";
                        totalBlockOrder.style.gridColumnEnd = "4";
                        let totalBlockMaintenance = document.getElementById("totalBlockMaintenance");
                        totalBlockMaintenance.style.gridColumnStart = "1";
                        totalBlockMaintenance.style.gridColumnEnd = "3";
                        let orderReport = document.querySelectorAll("#orderReport > div");
                        let maintenanceReport = document.querySelectorAll("#maintenanceReport > div");
                        orderReport.forEach(element => {
                            element.style.gridTemplateColumns = "12% 35% 25% 28%";
                        });
                        maintenanceReport.forEach(element => {
                            element.style.gridTemplateColumns = "25% 45% 30%";
                        });
                        let btnBack = document.getElementById("btnBack");
                        btnBack.addEventListener("click", () => {
                            window.location.href = "/report/";
                        });
                    }).catch(error => {
                        console.log(error);
                    });
                }).catch(error => {
                    console.log(error);
                });
            }
        }
        else if (choice.value == "monthlyReport") {
            if (yearSelected.value == "" || parseInt(yearSelected.value) > todayDate.getFullYear()) {
                alert("Invalid Year");
            } else {
                pageHeading.innerHTML = "MONTHLY REPORT";
                reportGrid.style.display = "none";
                actualReport.style.display = "grid";
                reportSection.style.margin = "1.5rem 5rem";
                async function getOrdersMonthly() {
                    const response = await fetch(`/getOrdersMonthly/${parseInt(monthSelected.value)}/${parseInt(yearSelected.value)}/`);
                    let data = await response.json();
                    return data;
                };
                async function getMaintenancesMonthly() {
                    const response = await fetch(`/getMaintenancesMonthly/${parseInt(monthSelected.value)}/${parseInt(yearSelected.value)}/`);
                    let data = await response.json();
                    return data;
                };
                let srNo = 1;
                let srNoMaintenance = 1;
                let orderCount = 0;
                let cash = 0;
                let online = 0;
                let maintenance = 0;
                let total = 0;
                getOrdersMonthly().then(data => {
                    let orderData = JSON.parse(data);
                    let stringToMonth = { "01": "January", "02": "February", "03": "March", "04": "April", "05": "May", "06": "June", "07": "July", "08": "August", "09": "Sepember", "10": "October", "11": "November", "12": "December" };
                    html += `<div id="monthlyReportdate">Month = ${stringToMonth[monthSelected.value]} ${yearSelected.value}</div>
                            <div id="Profit">
                                <div>
                                    <div id="cashTotal"></div>
                                </div>
                                <div>
                                    <div id="onlineTotal"></div>
                                </div>
                                <div>
                                    <div id="profitTotal"></div>
                                </div>
                                <div id="backbtnContainer">
                                    <button id="btnBack">
                                        <svg class="btnsvg" viewBox="0 0 100 100" width="1rem">
                                            <line class="line top" x1="10" x2="50" y1="70" y2="50" stroke="black" stroke-width="10" stroke-linecap="round"></line>
                                            <line class="line bottom" x1="10" x2="100" y1="70" y2="70" stroke="black" stroke-width="10" stroke-linecap="round"></line>
                                            <line class="line bottom" x1="10" x2="50" y1="70" y2="90" stroke="black" stroke-width="10" stroke-linecap="round"></line>
                                        </svg>
                                        <div>Back</div>
                                    </button>
                                </div>
                            </div>`;
                    orderHtml += `<div id="orderReport">
                            <div>
                                <div class="tableHeading borderTopLeft">Sr No</div>
                                <div class="tableHeading">Table No.</div>
                                <div class="tableHeading">Date</div>
                                <div class="tableHeading">Pay Type</div>
                                <div class="tableHeading borderTopRight noBorderRight">Amount</div>
                            </div>`;
                    if (orderData.allOrders.length == 0) {
                        orderHtml += `<div>
                                        <div class="paddingItems borderLeft borderRight" id="noDataOrder">No Records To Show</div>
                                    </div>`;
                    } else {
                        orderData.allOrders.forEach(element => {
                            let parsedQuantity = JSON.parse(element.quantity_items);
                            let titleItems = "";
                            Object.entries(parsedQuantity).forEach(item => {
                                let [key, value] = item;
                                let keyIndex = itemData.item_id.indexOf(parseInt(key));
                                titleItems += `${itemData.name[keyIndex]} ${itemData.item_size[keyIndex]} [${value}] `;
                            });
                            if (orderData.allOrders.length == srNo) {
                                orderHtml += `<div title="${titleItems}">
                                        <div class="paddingItems borderLeft borderRight">${srNo}</div>
                                        <div class="paddingItems borderRight">${element.name}</div>
                                        <div class="paddingItems borderRight">${element.date}</div>
                                        <div class="paddingItems borderRight">${element.payment_type}</div>
                                        <div class="paddingItems borderRight">${element.total}</div>
                                    </div>`;
                            } else {
                                orderHtml += `<div class="borderBottom" title="${titleItems}">
                                        <div class="paddingItems borderLeft borderRight">${srNo}</div>
                                        <div class="paddingItems borderRight">${element.name}</div>
                                        <div class="paddingItems borderRight">${element.date}</div>
                                        <div class="paddingItems borderRight">${element.payment_type}</div>
                                        <div class="paddingItems borderRight">${element.total}</div>
                                    </div>`;
                            }
                            if (element.payment_type == "Cash") {
                                cash += element.total;
                                total += element.total;
                            }
                            if (element.payment_type == "Online") {
                                online += element.total;
                                total += element.total;
                            }
                            orderCount++;
                            srNo++;
                        });
                    }
                    orderHtml += `<div>
                            <div class="tableHeading borderBottomLeft" id="totalBlockOrder">Total</div>
                            <div class="tableHeading borderBottomRight noBorderRight">${total}</div>
                        </div>
                        </div>`;
                    getMaintenancesMonthly().then(data => {
                        let maintenaceData = JSON.parse(data);
                        maintanaceHtml += `<div id="maintenanceReport">
                                        <div>
                                            <div class="tableHeading borderTopLeft">Sr No</div>
                                            <div class="tableHeading">Maintenance</div>
                                            <div class="tableHeading">Date</div>
                                            <div class="tableHeading borderTopRight noBorderRight">Amount</div>
                                        </div>`;
                        if (maintenaceData.allMaintenance.length == 0) {
                            maintanaceHtml += `<div>
                                                <div class="paddingItems borderLeft borderRight" id="noDataMaintenance">No Records To Show</div>
                                            </div>`;
                        } else {
                            maintenaceData.allMaintenance.forEach(element => {
                                if (maintenaceData.allMaintenance.length == srNoMaintenance) {
                                    maintanaceHtml += `<div>
                                                        <div class="paddingItems borderLeft borderRight">${srNoMaintenance}</div>
                                                        <div class="paddingItems borderRight">${element.name}</div>
                                                        <div class="paddingItems borderRight">${element.date}</div>
                                                        <div class="paddingItems borderRight">${element.price}</div>
                                                    </div>`;
                                } else {
                                    maintanaceHtml += `<div class="borderBottom">
                                                        <div class="paddingItems borderLeft borderRight">${srNoMaintenance}</div>
                                                        <div class="paddingItems borderRight">${element.name}</div>
                                                        <div class="paddingItems borderRight">${element.date}</div>
                                                        <div class="paddingItems borderRight">${element.price}</div>
                                                    </div>`;
                                }
                                maintenance += element.price;
                                srNoMaintenance++;
                            });
                        }
                        maintanaceHtml += `<div>
                                            <div class="tableHeading borderBottomLeft" id="totalBlockMaintenance">Total</div>
                                            <div class="tableHeading borderBottomRight noBorderRight">${maintenance}</div>
                                        </div>
                                        </div>`;
                        html += orderHtml;
                        html += maintanaceHtml;
                        actualReport.innerHTML += html;
                        let cashTotal = document.getElementById("cashTotal");
                        cashTotal.innerHTML = `Cash = ${cash}`;
                        let onlineTotal = document.getElementById("onlineTotal");
                        onlineTotal.innerHTML = `Online = ${online}`;
                        let profitTotal = document.getElementById("profitTotal");
                        profitTotal.innerHTML = `Profit = ${total - maintenance}`;
                        let noDataOrder = document.getElementById("noDataOrder");
                        if (noDataOrder != null) {
                            noDataOrder.style.gridColumnStart = "1";
                            noDataOrder.style.gridColumnEnd = "6";
                            noDataOrder.style.textAlign = "center";
                        }
                        let noDataMaintenance = document.getElementById("noDataMaintenance");
                        if (noDataMaintenance != null) {
                            noDataMaintenance.style.gridColumnStart = "1";
                            noDataMaintenance.style.gridColumnEnd = "5";
                            noDataMaintenance.style.textAlign = "center";
                        }
                        let totalBlockOrder = document.getElementById("totalBlockOrder");
                        totalBlockOrder.style.gridColumnStart = "1";
                        totalBlockOrder.style.gridColumnEnd = "5";
                        let totalBlockMaintenance = document.getElementById("totalBlockMaintenance");
                        totalBlockMaintenance.style.gridColumnStart = "1";
                        totalBlockMaintenance.style.gridColumnEnd = "4";
                        let btnBack = document.getElementById("btnBack");
                        btnBack.addEventListener("click", () => {
                            window.location.href = "/report/";
                        });
                    }).catch(error => {
                        console.log(error);
                    });
                }).catch(error => {
                    console.log(error);
                });
            }
        }
        else {
            if (yearSelected.value == "" || parseInt(yearSelected.value) > todayDate.getFullYear()) {
                alert("Invalid Year");
            } else {
                pageHeading.innerHTML = "YEARLY REPORT";
                reportGrid.style.display = "none";
                actualReport.style.display = "grid";
                reportSection.style.margin = "1.5rem 5rem";
                async function getOrdersYearly() {
                    const response = await fetch(`/getOrdersYearly/${parseInt(yearSelected.value)}/`);
                    let data = await response.json();
                    return data;
                };
                async function getMaintenancesYearly() {
                    const response = await fetch(`/getMaintenancesYearly/${parseInt(yearSelected.value)}/`);
                    let data = await response.json();
                    return data;
                };
                let srNo = 1;
                let srNoMaintenance = 1;
                let orderCount = 0;
                let cash = 0;
                let online = 0;
                let maintenance = 0;
                let total = 0;
                getOrdersYearly().then(data => {
                    let orderData = JSON.parse(data);
                    html += `<div id="yearlyReportdate">Year = ${yearSelected.value}</div>
                            <div id="Profit">
                                <div>
                                    <div id="cashTotal"></div>
                                </div>
                                <div>
                                    <div id="onlineTotal"></div>
                                </div>
                                <div>
                                    <div id="profitTotal"></div>
                                </div>
                                <div id="backbtnContainer">
                                    <button id="btnBack">
                                        <svg class="btnsvg" viewBox="0 0 100 100" width="1rem">
                                            <line class="line top" x1="10" x2="50" y1="70" y2="50" stroke="black" stroke-width="10" stroke-linecap="round"></line>
                                            <line class="line bottom" x1="10" x2="100" y1="70" y2="70" stroke="black" stroke-width="10" stroke-linecap="round"></line>
                                            <line class="line bottom" x1="10" x2="50" y1="70" y2="90" stroke="black" stroke-width="10" stroke-linecap="round"></line>
                                        </svg>
                                        <div>Back</div>
                                    </button>
                                </div>
                            </div>`;
                    orderHtml += `<div id="orderReport">
                            <div>
                                <div class="tableHeading borderTopLeft">Sr No</div>
                                <div class="tableHeading">Table No.</div>
                                <div class="tableHeading">Date</div>
                                <div class="tableHeading">Pay Type</div>
                                <div class="tableHeading borderTopRight noBorderRight">Amount</div>
                            </div>`;
                    if (orderData.allOrders.length == 0) {
                        orderHtml += `<div>
                                        <div class="paddingItems borderLeft borderRight" id="noDataOrder">No Records To Show</div>
                                    </div>`;
                    } else {
                        orderData.allOrders.forEach(element => {
                            let parsedQuantity = JSON.parse(element.quantity_items);
                            let titleItems = "";
                            Object.entries(parsedQuantity).forEach(item => {
                                let [key, value] = item;
                                let keyIndex = itemData.item_id.indexOf(parseInt(key));
                                titleItems += `${itemData.name[keyIndex]} ${itemData.item_size[keyIndex]} [${value}] `;
                            });
                            if (orderData.allOrders.length == srNo) {
                                orderHtml += `<div title="${titleItems}">
                                        <div class="paddingItems borderLeft borderRight">${srNo}</div>
                                        <div class="paddingItems borderRight">${element.name}</div>
                                        <div class="paddingItems borderRight">${element.date}</div>
                                        <div class="paddingItems borderRight">${element.payment_type}</div>
                                        <div class="paddingItems borderRight">${element.total}</div>
                                    </div>`;
                            } else {
                                orderHtml += `<div class="borderBottom" title="${titleItems}">
                                        <div class="paddingItems borderLeft borderRight">${srNo}</div>
                                        <div class="paddingItems borderRight">${element.name}</div>
                                        <div class="paddingItems borderRight">${element.date}</div>
                                        <div class="paddingItems borderRight">${element.payment_type}</div>
                                        <div class="paddingItems borderRight">${element.total}</div>
                                    </div>`;
                            }
                            if (element.payment_type == "Cash") {
                                cash += element.total;
                                total += element.total;
                            }
                            if (element.payment_type == "Online") {
                                online += element.total;
                                total += element.total;
                            }
                            orderCount++;
                            srNo++;
                        });
                    }
                    orderHtml += `<div>
                            <div class="tableHeading borderBottomLeft" id="totalBlockOrder">Total</div>
                            <div class="tableHeading borderBottomRight noBorderRight">${total}</div>
                        </div>
                        </div>`;
                    getMaintenancesYearly().then(data => {
                        let maintenaceData = JSON.parse(data);
                        maintanaceHtml += `<div id="maintenanceReport">
                                        <div>
                                            <div class="tableHeading borderTopLeft">Sr No</div>
                                            <div class="tableHeading">Maintenance</div>
                                            <div class="tableHeading">Date</div>
                                            <div class="tableHeading borderTopRight noBorderRight">Amount</div>
                                        </div>`;
                        if (maintenaceData.allMaintenance.length == 0) {
                            maintanaceHtml += `<div>
                                                <div class="paddingItems borderLeft borderRight" id="noDataMaintenance">No Records To Show</div>
                                            </div>`;
                        } else {
                            maintenaceData.allMaintenance.forEach(element => {
                                if (maintenaceData.allMaintenance.length == srNoMaintenance) {
                                    maintanaceHtml += `<div>
                                                        <div class="paddingItems borderLeft borderRight">${srNoMaintenance}</div>
                                                        <div class="paddingItems borderRight">${element.name}</div>
                                                        <div class="paddingItems borderRight">${element.date}</div>
                                                        <div class="paddingItems borderRight">${element.price}</div>
                                                    </div>`;
                                } else {
                                    maintanaceHtml += `<div class="borderBottom">
                                                        <div class="paddingItems borderLeft borderRight">${srNoMaintenance}</div>
                                                        <div class="paddingItems borderRight">${element.name}</div>
                                                        <div class="paddingItems borderRight">${element.date}</div>
                                                        <div class="paddingItems borderRight">${element.price}</div>
                                                    </div>`;
                                }
                                maintenance += element.price;
                                srNoMaintenance++;
                            });
                        }
                        maintanaceHtml += `<div>
                                            <div class="tableHeading borderBottomLeft" id="totalBlockMaintenance">Total</div>
                                            <div class="tableHeading borderBottomRight noBorderRight">${maintenance}</div>
                                        </div>
                                        </div>`;
                        html += orderHtml;
                        html += maintanaceHtml;
                        actualReport.innerHTML += html;
                        let cashTotal = document.getElementById("cashTotal");
                        cashTotal.innerHTML = `Cash = ${cash}`;
                        let onlineTotal = document.getElementById("onlineTotal");
                        onlineTotal.innerHTML = `Online = ${online}`;
                        let profitTotal = document.getElementById("profitTotal");
                        profitTotal.innerHTML = `Profit = ${total - maintenance}`;
                        let noDataOrder = document.getElementById("noDataOrder");
                        if (noDataOrder != null) {
                            noDataOrder.style.gridColumnStart = "1";
                            noDataOrder.style.gridColumnEnd = "6";
                            noDataOrder.style.textAlign = "center";
                        }
                        let noDataMaintenance = document.getElementById("noDataMaintenance");
                        if (noDataMaintenance != null) {
                            noDataMaintenance.style.gridColumnStart = "1";
                            noDataMaintenance.style.gridColumnEnd = "5";
                            noDataMaintenance.style.textAlign = "center";
                        }
                        let totalBlockOrder = document.getElementById("totalBlockOrder");
                        totalBlockOrder.style.gridColumnStart = "1";
                        totalBlockOrder.style.gridColumnEnd = "5";
                        let totalBlockMaintenance = document.getElementById("totalBlockMaintenance");
                        totalBlockMaintenance.style.gridColumnStart = "1";
                        totalBlockMaintenance.style.gridColumnEnd = "4";
                        let btnBack = document.getElementById("btnBack");
                        btnBack.addEventListener("click", () => {
                            window.location.href = "/report/";
                        });
                    }).catch(error => {
                        console.log(error);
                    });
                }).catch(error => {
                    console.log(error);
                });
            }
        }
    } else {
        let todayDate = new Date();
        if (choice.value == "dailyReport") {
            let dateSelectedObj = new Date(dateSelected.value);
            if (dateSelectedObj == "Invalid Date" || dateSelectedObj.getFullYear() > todayDate.getFullYear()) {
                alert("Invalid Date");
            } else {
                let date = "";
                let month = "";
                if (dateSelectedObj.getDate() < 10) {
                    date = `0${dateSelectedObj.getDate()}`;
                }
                else {
                    date = dateSelectedObj.getDate();
                }
                if (dateSelectedObj.getMonth() + 1 < 10) {
                    month = `0${dateSelectedObj.getMonth() + 1}`;
                } else {
                    month = dateSelectedObj.getMonth() + 1;
                }
                let url = `${window.location.origin}/getDailyReportByPDf/${date}${month}${dateSelectedObj.getFullYear()}/`;
                window.open(url,'_blank','popup=no');
            }
        } else if (choice.value == "monthlyReport") {
            if (yearSelected.value == "" || parseInt(yearSelected.value) > todayDate.getFullYear()) {
                alert("Invalid Year");
            } else {
                let url = `${window.location.origin}/getMonthlyReportByPDf/${parseInt(monthSelected.value)}/${parseInt(yearSelected.value)}/`;
                window.open(url,'_blank','popup=no');
            }
        }
        else {
            if (yearSelected.value == "" || parseInt(yearSelected.value) > todayDate.getFullYear()) {
                alert("Invalid Year");
            } else {
                let url = `${window.location.origin}/getYearlyReportByPDf/${parseInt(yearSelected.value)}/`;
                window.open(url,'_blank','popup=no');
            }
        }
    }
});