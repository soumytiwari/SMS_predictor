

let phone
let banks_info = []
let selected_account = ''
let got_bank_data = false
let got_bank_list = false
let got_trans_list = false
const showNavbar = (toggleId, navId, bodyId, headerId) => {
  const toggle = document.getElementById(toggleId),
    nav = document.getElementById(navId),
    bodypd = document.getElementById(bodyId),
    headerpd = document.getElementById(headerId)

  // Validate that all variables exist
  if (toggle && nav && bodypd && headerpd) {
    toggle.addEventListener('click', () => {
      // show navbar
      nav.classList.toggle('show')
      // change icon
      toggle.classList.toggle('bx-x')
      // add padding to body
      bodypd.classList.toggle('body-pd')
      // add padding to header
      headerpd.classList.toggle('body-pd')
    })
  }
}

document.addEventListener('DOMContentLoaded', () => {
  showNavbar('header-toggle', 'nav-bar', 'body-pd', 'header')

  fetch("/profile") // Replace "profile-url" with the actual URL to fetch profile data
    .then(response => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
    .then(data => {
      // Handle the profile data
      console.log(data);
      // Example: Accessing profile properties
      const name = data.name;
      const email = data.email;
      const address = data.address;
      phone = data.phone
      // Example: Updating HTML content with profile data
      document.getElementById("username").textContent = name;
      document.getElementById("email").textContent = email;
      document.getElementById("addr").textContent = address;
      document.getElementById("phone_no").textContent = phone;
    })
    .catch(error => {
      console.error("There was a problem with the fetch operation:", error);
    });
})


/*===== LINK ACTIVE =====*/
const linkColor = document.querySelectorAll('.nav_link')

function colorLink() {
  if (linkColor) {
    linkColor.forEach(l => {
      l.classList.remove('active')
      l.style.borderRight = ''
      document.getElementById(l.classList[0]).style.display = 'none'
    })
    let element = document.getElementById(this.classList[0])
    element.style.display = 'flex'
    element.style.flexDirection = 'column'
    this.classList.add('active');
    this.style.borderRight = '2px solid black';
    console.log(this)
  }
}
linkColor.forEach(l => l.addEventListener('click', colorLink))

function overview() {
  console.log('overview')
}

async function stats() {
  if (!got_bank_list) {
    await banks(); // Wait for banks data to be fetched
    const select_bank = document.getElementById('select-bank');
    console.log(banks_info.length);
    for (let index = 0; index < banks_info.length; index++) {
      const a = document.createElement('a')
      a.classList.add('drop-link');
      a.href = '#'
      let bank = banks_info[index]['Bank Name']
      let acc = banks_info[index]['Account No.']
      a.onclick = function () { selectValue(bank, acc) }
      a.innerHTML =
        `<span class="bnk-name">${bank}</span>
        <small class='acc-no'>A/C xxx${acc.substr(acc.length - 4)}</small>`;

      select_bank.appendChild(a);
    }
    got_bank_list = true;
  }
}


async function banks() {
  if (!got_bank_data) {
    try {
      const response = await fetch('/bank-info');
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const data = await response.json();

      // Define the order of keys/columns
      const columnOrder = ['Account No.', 'Customer Name', 'Bank Name', 'Phone Number', 'Balance'];

      const table = document.getElementById('usr_banks');
      data.forEach(entry => {
        banks_info.push(entry);
        const row = document.createElement('li');
        row.classList.add('table-row');
        let i = 1
        columnOrder.forEach(key => {
          const col = document.createElement('div');
          col.classList.add('col');
          col.classList.add(`col-${i}`);
          col.setAttribute('data-label', key);
          if (key === 'Account No.') {
            col.textContent = entry[key]; // Access the value using the key
          }
          else {
            col.textContent = entry[key]; // Access the value using the key
          }
          row.appendChild(col);
          i++
        });
        table.appendChild(row);
      });
      got_bank_data = true;
    } catch (error) {
      console.error('There was a problem with the fetch operation:', error);
    }
  }
}



function trans() {
  if (!got_trans_list) {
    fetch('/transactions')
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        const columnOrder = [
          'ID',
          'Acc. No.',
          'Date',
          'Time',
          'Amount',
          'Type',
        ];
        const table = document.getElementById('usr_trans');
        data.forEach(entry => {
          const row = document.createElement('li');
          row.classList.add('table-row');
          let i = 1
          columnOrder.forEach(key => {
            const col = document.createElement('div');
            col.classList.add('col');
            col.classList.add(`col-${i}`);
            col.setAttribute('data-label', key);
            col.textContent = entry[key]; // Access the value using the key
            row.appendChild(col);
            i++
          });
          table.appendChild(row);
        });
      })
      .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
      });
      got_trans_list = true
  }
}


function toggleDropdown() {
  document.querySelector('.dropdown').classList.toggle('active');
}

function selectValue(bank, acc) {
  if (!bank) {
    selected_account = 'ALL';
  }
  document.querySelector('.dropdown-input').value = bank;
  selected_account = acc;
  document.querySelector('.dropdown').classList.remove('active');
}

document.addEventListener('click', function (event) {
  var dropdown = document.querySelector('.dropdown');
  if (!dropdown.contains(event.target)) {
    dropdown.classList.remove('active');
  }
});

function Post(url, data) {
  fetch(url,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    })
    .then(response => {
      // Check if the response is successful
      if (response.ok) {
        // Redirect to the new page
        window.location.href = response.url;
      } else {
        // Handle error response
        console.error('Error:', response.statusText);
      }
    })
    .catch(error => {
      console.error('Error:', error);
    });
}


function annual_income() {
  console.log(selected_account)
  data = {
    'acc': selected_account,
    'phone': phone
  }
  Post('/annual-income', data)
}

function annual_saving() {
  data = {
    'acc': selected_account,
    'phone': phone
  }
  Post('/annual-savings', data)
}
function fav_bank() {
  data = {
    'acc': selected_account,
    'phone': phone
  }
  Post('/fav-bank', data)
}
function expensive_month() {
  data = {
    'acc': selected_account,
    'phone': phone
  }
  Post('/exp-month', data)
}
function credit_score() {
  data = {
    'acc': selected_account,
    'phone': phone
  }
  Post('/credit-score', data)
}
function max_trans() {
  data = {
    'acc': selected_account,
    'phone': phone
  }
  Post('/max-trans', data)
}