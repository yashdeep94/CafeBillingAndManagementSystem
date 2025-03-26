async function getitems(){
    const response = await fetch(`/getitems/`);
    let data = await response.json();
    return data;
};
let todayDate = new Date();
let date = "";
let month = "";
if (todayDate.getDate() < 10){
    date = `0${todayDate.getDate()}`;
}
else{
    date = todayDate.getDate();
}
if (todayDate.getMonth() + 1 < 10){
    month = `0${todayDate.getMonth() + 1}`;
}else{
    month = todayDate.getMonth() + 1;
}
async function getOrders(){
    const response = await fetch(`/getOrders/${date}${month}${todayDate.getFullYear()}/`);
    let data = await response.json();
    return data;
};
async function deleteOrder(orderId){
    const response = await fetch(`/deleteOrder/${orderId}/`);
    let data = await response.json();
    return data;
};
let manageOrderReport = document.getElementById("manageOrderReport");
let itemData;
getitems().then(d => {
    itemData = JSON.parse(d);
    getOrders().then(data => {
        let orderData = JSON.parse(data);
        let html = "";
        let srNo = 1;
        if (orderData.allOrders.length == 0){
            html += `<div>
                        <div class="paddingItems borderLeft borderRight borderBottom" id="noDataOrder">No Records To Show</div>
                    </div>`;
        }else{
            orderData.allOrders.forEach(element => {
                let parsedQuantity = JSON.parse(element.quantity_items);
                let orderItems = "";
                Object.entries(parsedQuantity).forEach(item => {
                    let [key, value] = item;
                    let keyIndex = itemData.item_id.indexOf(parseInt(key));
                    orderItems += `${itemData.name[keyIndex]} ${itemData.item_size[keyIndex]} [${value}] `;
                });
                html += `<div>
                            <div class="paddingItems borderBottom borderLeft borderRight">${srNo}</div>
                            <div class="paddingItems borderBottom borderRight">${element.name}</div>
                            <div class="paddingItems borderBottom borderRight">${orderItems}</div>
                            <div class="paddingItems borderBottom borderRight">${element.payment_type}</div>
                            <div class="paddingItems borderBottom borderRight">${element.total}</div>
                            <div class="paddingItems borderBottom borderRight centerAlign">
                                <img src="/static/images/trash.svg" alt="trash" id="${element.id}">
                                <img src="/static/images/edit-pen.png" alt="edit" id="edit${element.id}">
                            </div>
                        </div>`;
                srNo++;
            });
        }
        manageOrderReport.innerHTML += html;
        let deleteBtn = document.querySelectorAll(".centerAlign > img:first-child");
        deleteBtn.forEach(element => {
            element.addEventListener("click", (e) => {
                deleteOrder(e.target.id).then(status => {
                    let statusData = JSON.parse(status);
                    if (statusData.status == true){
                        alert("Order Deleted");
                        e.target.parentElement.parentElement.remove();
                        if (manageOrderReport.children.length == 1){
                            manageOrderReport.innerHTML += `<div>
                                        <div class="paddingItems borderLeft borderRight borderBottom" id="noDataOrder">No Records To Show</div>
                                    </div>`;
                        }
                    }
                }).catch(err => {
                    console.log(err);
                });
            });
        });
        let editBtn = document.querySelectorAll(".centerAlign > img:last-child");
        editBtn.forEach(element => {
            element.addEventListener("click", (e) => {
                window.location.href =  `/editOrder/${e.target.id.substring(4)}/`;
            });
        });
    }).catch(error => {
        console.log(error);
    });
}).catch(e => {
    console.log(e);
});