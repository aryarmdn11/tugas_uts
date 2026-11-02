document.addEventListener("DOMContentLoaded", function () {
  const sidebar = document.getElementById("sidebar");
  const overlay = document.getElementById("sidebar-overlay");
  const toggle = document.getElementById("sidebar-toggle");

  function tutupSidebar() {
    sidebar.classList.remove("show");
    overlay.classList.remove("show");
  }

  if (toggle && sidebar && overlay) {
    toggle.addEventListener("click", function () {
      sidebar.classList.toggle("show");
      overlay.classList.toggle("show");
    });
    overlay.addEventListener("click", tutupSidebar);
  }

  document.querySelectorAll(".alert-dismissible").forEach(function (el) {
    setTimeout(function () {
      bootstrap.Alert.getOrCreateInstance(el).close();
    }, 5000);
  });
});
