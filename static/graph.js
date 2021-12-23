let list = [];
async function check(url) {
    try {
        let res = await fetch(url)
        let status = await res.text(res)
        let obj = JSON.parse(status)
        let arr = obj.time
        let second, minute, hour, temp, cpy;

        for (let i = 0; i < arr.length; i++) {
            temp = arr[i]

            cpy = temp[6];
            cpy += temp[7];
            second = parseInt(cpy);
            cpy = temp[3];
            cpy += temp[4];
            minute = parseInt(cpy);
            cpy = temp[0];
            cpy += temp[1];
            hour = parseInt(cpy);

            temp = minute
            temp += second / 60;
            temp += 60 * hour;
            list[i] = temp
        }
        console.log(list);
        new Chart(document.getElementById("line-chart"), {
            type: 'line',
            data: {
                labels: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                datasets: [{
                    data: list,
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
        return list;
    }
    catch {
        console.log("faild")
    }
}
check("http://10.150.150.1:5000/history")