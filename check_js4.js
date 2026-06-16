const fs = require('fs');
const content = fs.readFileSync('static/xhs_main_260411.js', 'utf-8');
const lines = content.split('\n');
const line78 = lines[77];

const match = line78.match(/"redmoji": "(\{.*\})"/);
if (match) {
    const jsonStr = match[1];
    try {
        const parsed = JSON.parse(jsonStr);
        console.log('JSON parse success!');
        console.log('redmojiTabs count:', parsed.redmojiTabs?.length);
        console.log('redmojiMap keys count:', Object.keys(parsed.redmojiMap || {}).length);
    } catch (e) {
        console.log('JSON parse error:', e.message);
        
        const jsonStr2 = match[1];
        const colonCount = (jsonStr2.match(/:/g) || []).length;
        const quoteCount = (jsonStr2.match(/"/g) || []).length;
        console.log('Colon count in JSON:', colonCount);
        console.log('Quote count in JSON:', quoteCount);
        
        const parts = jsonStr2.split('":"');
        console.log('Parts separated by ":" count:', parts.length);
        
        for (let i = 0; i < parts.length; i++) {
            const part = parts[i];
            if (i > 0) {
                const prevPart = parts[i - 1];
                const lastChar = prevPart.slice(-1);
                if (lastChar !== '"') {
                    console.log(`Part ${i}: previous part doesn't end with quote`);
                    console.log(`  Previous part ends with: '${prevPart.slice(-20)}'`);
                }
            }
            if (i < parts.length - 1) {
                const nextPart = parts[i + 1];
                const firstChar = nextPart.slice(0, 1);
                if (firstChar !== '"') {
                    console.log(`Part ${i}: next part doesn't start with quote`);
                    console.log(`  Next part starts with: '${nextPart.slice(0, 20)}'`);
                }
            }
        }
    }
} else {
    console.log('No match found for redmoji');
}