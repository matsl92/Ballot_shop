const data = JSON.parse(
    document.getElementById('context-variables').textContent
);

console.log(data);

const toastTrigger = data.msg[0];

const toastLiveExample = document.getElementById('notification');
const toast = new bootstrap.Toast(toastLiveExample,{
    delay: 10000
});
const link = "{{ link|safe }}"

if (toastTrigger == 'suc') {
  toastLiveExample.classList.remove("bg-danger");
  toastLiveExample.classList.remove("bg-warning");
  toastLiveExample.classList.remove("bg-success");
  toastLiveExample.classList.add("bg-success");
  
  toastLiveExample.innerHTML = `
    <div class="toast-header">
      <i class="bi bi-check"></i>
      <strong class="me-auto"> ¡Felicidades!</strong>
      <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
    </div>
    <div class="toast-body text-white">
      ${data.msg[1]}
    </div>
  `;

  toast.show();

} else if (toastTrigger == 'err' &&  data.link ) {
  toastLiveExample.classList.remove("bg-danger");
  toastLiveExample.classList.remove("bg-warning");
  toastLiveExample.classList.remove("bg-success");
  toastLiveExample.classList.add("bg-danger");
  
  toastLiveExample.innerHTML = `
    <div class="toast-header">
      <i class="bi bi-x"></i>
      <strong class="me-auto"> Lo sentimos</strong>
      <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
    </div>
    <div class="toast-body text-white">
      ${data.msg[1]}<a href="${data.link}" style="color: #fff;"><strong>aquí</strong></a>
    </div>
  `;

  toast.show();

} else if (toastTrigger == 'err') {
    toastLiveExample.classList.remove("bg-danger");
    toastLiveExample.classList.remove("bg-warning");
    toastLiveExample.classList.remove("bg-success");
    toastLiveExample.classList.add("bg-danger");
    
    toastLiveExample.innerHTML = `
      <div class="toast-header">
        <i class="bi bi-x"></i>
        <strong class="me-auto"> Lo sentimos</strong>
        <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
      </div>
      <div class="toast-body text-white">
        ${data.msg[1]}
      </div>
    `;
  
    toast.show();

}  else if (toastTrigger == 'war') {
    toastLiveExample.classList.remove("bg-danger");
    toastLiveExample.classList.remove("bg-warning");
    toastLiveExample.classList.remove("bg-success");
    toastLiveExample.classList.add("bg-warning");
    
    toastLiveExample.innerHTML = `
      <div class="toast-header">
        <i class="bi bi-exclamation-triangle-fill"></i>
        <strong class="me-auto">  Alerta</strong>
        <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
      </div>
      <div class="toast-body text-white">
        ${data.msg[1]}
      </div>
    `;
  
    toast.show();
  }





