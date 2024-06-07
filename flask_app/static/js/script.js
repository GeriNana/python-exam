document.getElementById('menuToggle').addEventListener('click', function() {
    document.getElementById('dropdownMenu').classList.toggle('active');
});

// Function to change language
function changeLanguage(language) {
    if (language === 'sq') {
        document.querySelector('.courier-link').textContent = 'Bëhu Korrier';
        document.querySelector('.dropdown-row a[href="login.html"]').textContent = 'Hyr';
        document.querySelector('.dropdown-row a[href="register.html"]').textContent = 'Regjistrohu';
        document.querySelector('.dropdown-menu a[href="help.html"]').textContent = 'Keni nevojë për ndihmë?';
        document.querySelector('.hero-content h1').textContent = 'Plotësoni dëshirat tuaja në çdo kohë';
        document.querySelector('.hero-content p').textContent = 'Eksploroni restorantet dhe dyqanet në zonën tuaj që ofrojnë shërbime të dorëzimit.';
        document.querySelector('.search-bar input[type="text"]').placeholder = 'Shkruani qytetin tuaj';
        document.querySelector('.search-bar button').textContent = 'Kërko';
        document.querySelector('.how-to-order h2').textContent = 'Si të porosisni';
        document.querySelectorAll('.step h3')[0].textContent = 'Zbuloni Vendndodhjen Tuaj';
        document.querySelectorAll('.step p')[0].textContent = 'Thjesht shkruani adresën tuaj dhe eksploroni pikat më të mira ushqimore rreth jush.';
        document.querySelectorAll('.step h3')[1].textContent = 'Eksploroni Menu';
        document.querySelectorAll('.step p')[1].textContent = 'Shfletoni një shumëllojshmëri pjatash dhe gjeni atë që ju kënaq më shumë.';
        document.querySelectorAll('.step h3')[2].textContent = 'Porosisni dhe Kënaquni';
        document.querySelectorAll('.step p')[2].textContent = 'Zgjidhni dorëzimin ose marrjen, dhe ne do t\'ju informojmë në çdo hap të procesit.';
    } else {
        document.querySelector('.courier-link').textContent = 'Become a Courier';
        document.querySelector('.dropdown-row a[href="login.html"]').textContent = 'Login';
        document.querySelector('.dropdown-row a[href="register.html"]').textContent = 'Register';
        document.querySelector('.dropdown-menu a[href="help.html"]').textContent = 'Need Help?';
        document.querySelector('.hero-content h1').textContent = 'Satisfy Your Cravings Anytime';
        document.querySelector('.hero-content p').textContent = 'Explore restaurants and stores in your area offering delivery services.';
        document.querySelector('.search-bar input[type="text"]').placeholder = 'Enter your city';
        document.querySelector('.search-bar button').textContent = 'Search';
        document.querySelector('.how-to-order h2').textContent = 'How to Order';
        document.querySelectorAll('.step h3')[0].textContent = 'Discover Your Location';
        document.querySelectorAll('.step p')[0].textContent = 'Simply input your address and explore the best food spots around you.';
        document.querySelectorAll('.step h3')[1].textContent = 'Explore Menus';
        document.querySelectorAll('.step p')[1].textContent = 'Browse a variety of dishes and find what satisfies your cravings.';
        document.querySelectorAll('.step h3')[2].textContent = 'Order and Enjoy';
        document.querySelectorAll('.step p')[2].textContent = 'Choose delivery or pickup, and we\'ll keep you updated every step of the way.';
    }
}

// Event listener for language selection
document.getElementById('languageSelect').addEventListener('change', function() {
    const selectedLanguage = this.value;
    localStorage.setItem('preferredLanguage', selectedLanguage);
    changeLanguage(selectedLanguage);
});

// Check for saved language preference on load
document.addEventListener('DOMContentLoaded', function() {
    const preferredLanguage = localStorage.getItem('preferredLanguage') || 'en';
    document.getElementById('languageSelect').value = preferredLanguage;
    changeLanguage(preferredLanguage);
});
