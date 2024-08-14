// 引入Quantumult X的环境变量处理库
const env = $environment;

// 检查pgsh_data环境变量
if (env && env.pgsh_data) {
    console.log("pgsh_data 内容:", env.pgsh_data);
    // 可以将内容输出到控制台或直接返回给客户端
    $done({
        response: {
            status: 200,
            body: JSON.stringify({
                message: "pgsh_data 内容",
                data: env.pgsh_data
            })
        }
    });
} else {
    console.log("pgsh_data 环境变量未定义");
    $done({
        response: {
            status: 500,
            body: JSON.stringify({
                message: "pgsh_data 环境变量未定义"
            })
        }
    });
}
