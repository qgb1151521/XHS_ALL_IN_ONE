const fs = require('fs');
const code = fs.readFileSync('static/xhs_main_260411.js', 'utf-8');

try {
    eval(code);
    console.log('Eval successful');
} catch (e) {
    console.log('Eval error:', e.message);
    console.log('Stack:', e.stack);
    process.exit(1);
}

try {
    console.log('Calling get_request_headers_params...');
    const result = get_request_headers_params('/api/test', '', 'test_a1_cookie');
    console.log('Function call success!');
    console.log('Result:', result);
} catch (e) {
    console.log('Function call error:', e.message);
    console.log('Stack:', e.stack);
}