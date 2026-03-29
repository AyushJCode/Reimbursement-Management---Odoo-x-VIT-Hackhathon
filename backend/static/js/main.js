// --- 1. UTILS ---
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email.toLowerCase());
}

// 🛡️ New: Prevent numbers in names
function validateName(name) {
    const re = /^[a-zA-Z\s]*$/;
    return re.test(name) && name.length > 2;
}

function toggleAuth(isRegister) {
    document.getElementById('loginForm').classList.toggle('hidden', isRegister);
    document.getElementById('registerForm').classList.toggle('hidden', !isRegister);
    document.getElementById('authSubtext').innerText = isRegister ? "REGISTER YOUR COMPANY" : "REIMBURSEMENT PORTAL";
}

// --- 2. AUTHENTICATION ---
async function login() {
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;

    const res = await fetch('/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
    });

    const data = await res.json();
    if (res.ok) {
        localStorage.setItem('user_name', data.name); // Store name for UI
        setupDashboard(data);
    } else {
        alert(data.error || "Invalid Credentials");
    }
}

async function register() {
    const name = document.getElementById('regName').value.trim();
    const email = document.getElementById('regEmail').value.trim();
    
    if (!validateName(name)) {
        alert("Please enter a valid name (letters only, min 3 chars).");
        return;
    }
    if (!validateEmail(email)) {
        alert("Please provide a valid email address.");
        return;
    }

    const payload = {
        name: name,
        email: email,
        password: document.getElementById('regPassword').value,
        company_name: document.getElementById('regCompany').value,
        currency_code: document.getElementById('regCurrency').value
    };

    const res = await fetch('/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    });

    if (res.ok) {
        alert("Success! Your Company is registered. Please login.");
        toggleAuth(false);
    } else {
        const data = await res.json();
        alert(data.error || "Registration failed");
    }
}

function setupDashboard(data) {
    document.getElementById('loginSection').classList.add('hidden');
    document.getElementById('dashboard').classList.remove('hidden');
    // Display the Name instead of the ID
    document.getElementById('welcomeMsg').innerText = `Welcome, ${data.name}`;
    
    if (data.role === 'Admin' || data.role === 'Manager') {
        document.getElementById('managerSection').classList.remove('hidden');
        loadPending();
    }
    loadHistory();
}

// --- 3. EXPENSE & REPORTS ---
async function loadHistory() {
    const res = await fetch('/expenses/my-history');
    const data = await res.json();
    const tbody = document.querySelector('#histTable tbody');
    tbody.innerHTML = data.map(ex => `
        <tr>
            <td>${ex.date}</td>
            <td class="fw-bold">${ex.category}</td>
            <td>${ex.currency} ${ex.amount}</td>
            <td><span class="status-${ex.status.toLowerCase()}">${ex.status}</span></td>
        </tr>
    `).join('');
}

async function loadPending() {
    // 💡 Note: Your backend /approvals/pending route should join with the users table 
    // to provide 'employee_name'. If it doesn't, it will default to "Employee"
    const res = await fetch('/approvals/pending');
    const data = await res.json();
    const container = document.getElementById('pendTable');
    
    if (data.length === 0) {
        container.innerHTML = '<p class="text-center py-4 small text-muted">All caught up! ✅</p>';
        return;
    }

    container.innerHTML = data.map(ex => `
        <div class="card mb-3 p-3 border-0 shadow-sm border-start border-4 border-primary">
            <div class="d-flex justify-content-between mb-1">
                <span class="fw-bold text-dark">${ex.category}</span>
                <span class="text-success fw-bold">₹${ex.converted_amount}</span>
            </div>
            <p class="tiny text-muted mb-3">Submitted by: ${ex.employee_name || 'Team Member'}</p>
            <div class="d-flex gap-2">
                <button onclick="handleAction(${ex.id}, 'approve')" class="btn btn-sm btn-success w-50">Approve</button>
                <button onclick="handleAction(${ex.id}, 'reject')" class="btn btn-sm btn-outline-danger w-50">Reject</button>
            </div>
        </div>
    `).join('');
}

async function handleAction(id, action) {
    await fetch('/approvals/action', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ expense_id: id, action: action })
    });
    loadPending();
    loadHistory();
}

async function showReports() {
    const res = await fetch('/expenses/stats');
    const data = await res.json();
    const tbody = document.querySelector('#histTable tbody');
    document.getElementById('welcomeMsg').innerText = "Expense Analytics";
    
    tbody.innerHTML = data.map(s => `
        <tr><td>-</td><td class="fw-bold text-primary">${s.category}</td><td>₹${s.total}</td><td><span class="status-approved">REPORT</span></td></tr>
    `).join('');
}

// --- 4. FORM SUBMISSION ---
document.getElementById('expForm').onsubmit = async (e) => {
    e.preventDefault();
    const res = await fetch('/expenses/add-expense', { method: 'POST', body: new FormData(e.target) });
    if (res.ok) {
        bootstrap.Modal.getInstance(document.getElementById('expenseModal')).hide();
        e.target.reset();
        loadHistory();
        loadPending();
    }
};