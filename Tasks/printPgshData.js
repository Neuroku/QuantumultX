// Quantumult X script to output the content of the environment variable pgsh_data
// The script is triggered by a specific URL matching rule

// Fetch the environment variable pgsh_data
let pgshData = $persistentStore.read("pgsh_data");

// Check if pgsh_data exists
if (pgshData) {
    console.log("pgsh_data 内容:", pgshData);
    // Modify the request body or respond with the pgsh_data content
    $done({ 
        response: { 
            status: 200, 
            body: pgshData 
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
