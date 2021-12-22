const img = document.querySelector(".image"); //이미지 파일
const sw1 = document.querySelector(".div3-1");
const sw2 = document.querySelector(".div3-2");

  async function check(url) {
       try {
	   let res = await fetch(url);
	   let status = await res.text();
	   if (status == '1') {
		img.src="../static/images/high.png";
		sw1.style.display = 'none';
		sw2.style.display = 'block';
	   } else if (status=='0') {
		img.src="../static/images/low.png";
		sw1.style.display = 'block';
		sw2.style.display = 'none';
	   } else {
		alert("상태를 받아 올 수 없습니다");
	   }
       }
       catch {
	   console.log("faild");
       }
  }

  check("http://10.150.150.1:5000/check");

  sw1.addEventListener("click", ()=> {
    img.src = "../static/images/high.png";
    sw1.style.display = 'none';
    sw2.style.display = 'block';
    fetch("http://10.150.150.1:5000/led/on").then((response) =>
      console.log(response)
    );
    //서버로 보내는거 키는거
  })
  sw2.addEventListener("click", ()=> {
    //서버로 보내는거 끄는거
    img.src = "../static/images/low.png";
    sw1.style.display = 'block';
    sw2.style.display = 'none';
    fetch("http://10.150.150.1:5000/led/off").then((response) =>
      console.log(response)
    );
  })