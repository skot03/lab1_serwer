function newDiv(responseData) {
    let responseContainer = document.querySelector('.members');
    let response_item = document.createElement('div');
    response_item.classList.add('item');
    responseContainer.appendChild(response_item);

    let info = document.createElement('div');
    info.classList.add('info');
    response_item.appendChild(info);

    let response_fullname = document.createElement('div');
    response_fullname.textContent = responseData['first_name'] + ' ' + responseData['last_name'];
    response_fullname.classList.add('fullname');
    info.appendChild(response_fullname);

    let response_role = document.createElement('div');
    response_role.textContent = responseData['role'];
    response_role.classList.add('response-role');
    info.appendChild(response_role);


    let delete_img = document.createElement('img');
    delete_img.src = 'delete.png';
    delete_img.classList.add('delete-img');
    delete_img.addEventListener('click', () => {
        response_item.remove();
        sendDeleteRequest(responseData);
    });
    response_item.appendChild(delete_img);
   
    
    
}

async function sendGetRequest() {
    try {
        const response = await fetch('http://localhost:8000/');
        const responseData = await response.json();
        responseData.forEach((data) => {
            newDiv(data);
        });
    } catch (error) {
        console.error('Error:', error);
    }
}

async function sendPostRequest(data) {
    try {
        const response = await fetch('http://localhost:8000/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        const responseData = await response.json();
        newDiv(responseData);
    } catch (error) {
        console.error('Error:', error);
    }
}

async function sendDeleteRequest(data) {
    try {
        const response = await fetch('http://localhost:8000/', {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        const responseData = await response.json();
        console.log(responseData);
    } catch (error) {
        console.error('Error:', error);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    sendGetRequest();

    let myform = document.getElementById('myform');
    if (myform) {
        myform.addEventListener('submit', async (event) => {
            event.preventDefault();
            console.log('myform submission started');
            const data = { 
                first_name: document.getElementById('first_name').value, 
                last_name: document.getElementById('last_name').value,
                role: document.getElementById('role').value
            };
            sendPostRequest(data);
        })
    }
    else {
        console.error('myform not found');
    }
});