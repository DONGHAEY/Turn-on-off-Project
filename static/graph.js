let list = [];
async function check(url) {
    try {
        let res = await fetch(url)
        let status = await res.text(res)
        let obj = JSON.parse(status)
        let arr = obj.time
        let second, minute, hour, temp, cpy;

        for (let i = 0; i < arr.length; i++) {
//arr = ["00:00:00", "00:00:00", "00:00:00"] 서버에서 제공하는 형식이다 
//켜져있던 시간이 서버에서 string 형태로 제공된다
            temp = arr[i] //여러 시간들중 i번째

            cpy = temp[6]; //초의 10의자리
            cpy += temp[7]; //초의 1의자리
            second = parseInt(cpy); //초를 숫자로 바꾼다
            cpy = temp[3]; //분의 10의자리
            cpy += temp[4]; //분의 1의자리
            minute = parseInt(cpy); //분을 숫자로 바꾼다
            cpy = temp[0]; //시간의 10의자리
            cpy += temp[1]; //시간의 1의자리
            hour = parseInt(cpy); //시간을 숫자로 바꾼다
//분단위 계산알고리즘
            temp = minute
            temp += second / 60;
            temp += 60 * hour;
            list[i] = temp //분의 단위로 계산된 숫자가 list array에 저장된다
        }
        console.log(list);

        new Chart(document.getElementById("line-chart"), { //차트 객체를 만든다
            type: 'line',
            data: {
                labels: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                datasets: [{
                    data: list, //이곳에 가공한 코드를 넣는다
                    label: "LED USING TIME",
                    borderColor: "#3e95cd",
                    fill: false
                }
                ]
            },
            options: {
                title: {
                    display: true,
                    text: '조명 사용 시간도'
                }
            }
        });
        return list; //차트 객체를 반환한다
    }
    catch {
        console.log("faild")
    }
}
check("http://10.150.150.1:5000/history")
