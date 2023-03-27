console.log('hello world');

// const data = document.currentScript.dataset;
// const followerCount = data.followerCount;
// console.log(followerCount);

const jsVariables = JSON.parse(
    document.currentScript.nextElementSibling.textContent
  );
console.log(jsVariables);
