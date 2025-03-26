let btn=document.getElementById('hamburger');
let main=document.getElementById('main');
let left=document.getElementById('left');
let navigation=document.getElementById('navigation');
let addressBarLocation= window.location.pathname;
if (addressBarLocation=='/'){
    let home=document.querySelector("#navigation >button > a:first-child");
    home.style.color='var(--black)';
    home.parentElement.style.backgroundColor='var(--yellow)';
    home.parentElement.style.border='1px solid var(--black)';
}else if(addressBarLocation=='/order/'){
    let order=document.getElementById("changeOrderNav");
    order.style.color='var(--black)';
    order.parentElement.style.backgroundColor='var(--yellow)';
    order.parentElement.style.border='1px solid var(--black)';
}
else if(addressBarLocation=='/manageOrders/'){
    let manageOrder=document.getElementById("changeManOrderNav");
    manageOrder.style.color='var(--black)';
    manageOrder.parentElement.style.backgroundColor='var(--yellow)';
    manageOrder.parentElement.style.border='1px solid var(--black)';
}
else if(addressBarLocation=='/report/'){
    let report=document.getElementById("changeReportNav");
    report.style.color='var(--black)';
    report.parentElement.style.backgroundColor='var(--yellow)';
    report.parentElement.style.border='1px solid var(--black)';
}
else if(addressBarLocation=='/additem/'){
    let addItem=document.getElementById("changeAddItemNav");
    addItem.style.color='var(--black)';
    addItem.parentElement.style.backgroundColor='var(--yellow)';
    addItem.parentElement.style.border='1px solid var(--black)';
}
else if(addressBarLocation=='/maintenance/'){
    let maintenance=document.getElementById("changeMaintenanceNav");
    maintenance.style.color='var(--black)';
    maintenance.parentElement.style.backgroundColor='var(--yellow)';
    maintenance.parentElement.style.border='1px solid var(--black)';
}
let defaultMainTemplateColums = main.style.gridTemplateColumns;
let defaultMainTemplatRows = main.style.gridTemplateRows;
btn.addEventListener('click',()=>{
    btn.classList.toggle('clicked');
    if (window.innerWidth <= 750){
        if(btn.classList.length==0){
            navigation.style.display='none';
            left.style.gridTemplateRows='auto';
            main.style.gridTemplateRows=defaultMainTemplatRows;
        }else{
            left.style.gridTemplateRows='auto auto';
            main.style.gridTemplateRows='auto 20% auto';
            setTimeout(()=>{
                navigation.style.display='grid';
            },250); 
        }
    }
    else if (window.innerWidth <= 1000){
        if(btn.classList.length==0){
            navigation.style.display='none';
            left.style.gridTemplateRows='auto';
            main.style.gridTemplateRows=defaultMainTemplatRows;
        }else{
            left.style.gridTemplateRows='auto auto';
            main.style.gridTemplateRows='auto 20% auto';
            setTimeout(()=>{
                navigation.style.display='grid';
            },250); 
        }
    }else{
        if(btn.classList.length==0){
            navigation.style.display='none';
            left.style.gridTemplateColumns='auto';
            main.style.gridTemplateColumns=defaultMainTemplateColums;
        }else{
            navigation.style.display='grid';
            left.style.gridTemplateColumns='80% 20%';
            main.style.gridTemplateColumns='20% auto';
        }
    }
});
