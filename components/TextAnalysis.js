import React, { useState } from 'react';
import { analyzeText } from './apiService';

const TextAnalysis = () => {
    const [text, setText] = useState('');
    const [analysis, setAnalysis] = useState('');

    const handleAnalyze = async () => {
        const result = await analyzeText(text);
        setAnalysis(result.analysis);
    };

    return (
        <div>
            <textarea value={text} onChange={(e) => setText(e.target.value)} />
            <button onClick={[_{{{CITATION{{{_1{](https://github.com/shivendrakmr05/blossom/tree/ad523cff6e9f1be73949ee9fc815f5ae8751e73e/equipment.php)[_{{{CITATION{{{_2{](https://github.com/ravisingh2811/Excellence/tree/d0fc139aed78df0ce5ab1a0bf68c2cc8ed84fb4d/admin_login.php)[_{{{CITATION{{{_3{](https://github.com/Tayeb-Ali/vPurchase/tree/5ab5d982b3e607a092abd2e2052ced5d50f391d5/resources%2Fviews%2Findex.blade.php)[_{{{CITATION{{{_4{](https://github.com/smgmode/p2_ADVWEB_Glover_Stephanie/tree/b77fa0366dccc991b8b19e7c1ed038b866abf841/form%2Fdefault.inc.php)[_{{{CITATION{{{_5{](https://github.com/Dangereye/portfolio-njs/tree/34c4218add1c2a88c425f0b520514051a42ae209/Contact.js)[_{{{CITATION{{{_6{](https://github.com/suyashpradhan/machine-coding-practice/tree/15fe5ad3c4aaec2c5e79c13a64934c17f5810d89/src%2FFastMart%2Fcontext%2Fstate-context.js)[_{{{CITATION{{{_7{](https://github.com/AlexandrDrachev/todo/tree/4901e62a9db15274e606038d5051fa0d62132480/src%2Fstate%2Findex.js)[_{{{CITATION{{{_8{](https://github.com/ViniSpirit/vini-blog/tree/bcd15776049ae9b7baec7a2d21cbba2b86cdb35a/pages%2Fusers%2Flogin.js)[_{{{CITATION{{{_9{](https://github.com/aostrowicki/jwt-with-redux/tree/3b9152cc6d09944c4e3f78abec06f12060d2ce9a/client%2Fsrc%2Fviews%2FLogin.js)
