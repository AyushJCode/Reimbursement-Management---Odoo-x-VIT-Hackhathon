// --- 1. Login Logic ---
async function login() {
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    if (!email || !password) {
        alert("Please fill in all fields.");
        return;
    }

    try {
        const res = await fetch('/auth/login', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ email, password })
        });

        const data = await res.json();
        
        if (res.ok) {
            document.getElementById('loginSection').classList.add('hidden');
            document.getElementById('dashboard').classList.remove('hidden');
            document.getElementById('welcomeMsg').innerText = `Odoo | ${data.role}`;
            
            // Show Manager section if authorized
            if (data.role === 'Admin' || data.role === 'Manager') {
                document.getElementById('managerSection').classList.remove('hidden');
                loadPending();
            }
            loadHistory();
        } else {
            alert(data.error || "Invalid Credentials");
        }
    } catch (err) {
        console.error("Login Error:", err);
    }
}

// --- 2. Load Expense History ---
async function loadHistory() {
    const res = await fetch('/expenses/my-history');
    const data = await res.json();
    const tbody = document.querySelector('#histTable tbody');
    
    tbody.innerHTML = data.map(ex => `
        <tr>
            <td class="small">${ex.date}</td>
            <td><span class="fw-bold">${ex.category}</span></td>
            <td>${ex.currency} ${ex.amount}</td>
            <td><span class="status-${ex.status.toLowerCase()}">${ex.status}</span></td>
        </tr>
    `).join('');
}

// --- 3. Load Manager Approvals ---
async function loadPending() {
    const res = await fetch('/approvals/pending');
    const data = await res.json();
    const container = document.getElementById('pendTable');
    
    if (data.length === 0) {
        container.innerHTML = '<p class="text-muted text-center py-3">No pending claims</p>';
        return;
    }

    container.innerHTML = data.map(ex => `
        <div class="card mb-3 shadow-sm border-0">
            <div class="card-body">
                <div class="d-flex justify-content-between mb-2">
                    <span class="fw-bold">${ex.category}</span>
                    <span class="text-success fw-bold">₹${ex.converted_amount}</span>
                </div>
                <p class="small text-muted mb-3">${ex.description || 'No description provided'}</p>
                <div class="d-flex gap-2">
                    <button onclick="handleAction(${ex.id}, 'approve')" class="btn btn-sm btn-success w-100">Approve</button>
                    <button onclick="handleAction(${ex.id}, 'reject')" class="btn btn-sm btn-outline-danger w-100">Reject</button>
                </div>
            </div>
        </div>
    `).join('');
}

// --- 4. Approve/Reject Action ---
async function handleAction(id, action) {
    const res = await fetch('/approvals/action', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ expense_id: id, action: action })
    });

    if (res.ok) {
        loadPending();
        loadHistory();
    }
}

// --- 5. Submit New Expense ---
document.getElementById('expForm').onsubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    
    const res = await fetch('/expenses/add-expense', {
        method: 'POST',
        body: formData
    });

    if (res.ok) {
        const modal = bootstrap.Modal.getInstance(document.getElementById('expenseModal'));
        modal.hide();
        e.target.reset();
        alert("Expense submitted for review!");
        loadHistory();
        loadPending();
    } else {
        alert("Error submitting expense.");
    }
};