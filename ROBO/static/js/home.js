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
async function getMaintenances(){
    const response = await fetch(`/getMaintenances/${date}${month}${todayDate.getFullYear()}/`);
    let data = await response.json();
    return data;
};
let homeOrder = document.getElementById("homeOrder");
let incomeCash = document.getElementById("incomeCash");
let incomeOnline = document.getElementById("incomeOnline");
let homeMaintenance = document.getElementById("homeMaintenance");
let orderCount = 0;
let cash = 0;
let online = 0;
let maintenance = 0;
getOrders().then(data => {
    let orderData = JSON.parse(data);
    orderData.allOrders.forEach(element => {
        if (element.payment_type == "Cash"){
            cash += element.total;
        }
        if (element.payment_type == "Online"){
            online += element.total;
        }
        orderCount++;
    });
    homeOrder.innerHTML = orderCount;
    incomeCash.innerHTML = cash;
    incomeOnline.innerHTML = online;
}).catch(error => {
    console.log(error);
});
getMaintenances().then(data => {
    let maintenaceData = JSON.parse(data);
    maintenaceData.allMaintenance.forEach(element => {
        maintenance += element.price;
    });
    homeMaintenance.innerHTML += maintenance;
}).catch(error => {
    console.log(error);
});