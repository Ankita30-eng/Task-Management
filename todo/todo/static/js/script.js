// Optional small effects
document.addEventListener("DOMContentLoaded", () => {
  const todos = document.querySelectorAll(".todo-item");
  todos.forEach(todo => {
    todo.addEventListener("mouseenter", () => {
      todo.style.backgroundColor = "#f8f9fa";
    });
    todo.addEventListener("mouseleave", () => {
      todo.style.backgroundColor = "white";
    });
  });
});