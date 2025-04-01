<p>The repo is about graph theory. It works with tabular data and apply Social Network Analysis (SNA) technique to visualise the networks and generates statistical modelling. The assumed persona of the users are Social network researchers and data analysts</p>
<p>An external Git repo https://github.com/stivalaa/ALAAMEE is incorporated for the ALAAMEE algrothrim. Reference: Stivala, A., Wang, P., & Lomi, A. (2024). ALAAMEE: Open-source software for fitting autologistic actor attribute models. PLOS Complex Systems 1(4):e0000021. https://doi.org/10.1371/journal.pcsy.0000021</p>

<h4>Environment and dependencies</h4>
<h4>Frontend</h4>
<ol>
  <li>React.js with Vite</li>
  <li>Material UI (day 2 implementation)</li>
</ol>
<h2>Backend</h2>
<ul>
  <li>Flask</li>
  <ul>
    <li>Key libraries used: Pandas, Numpy, Matplotlib, Scipy, Scikit-learn</li>
    <li><em>Codes form an external Git repo https://github.com/stivalaa/ALAAMEE is extracted and included in this repo</em></li>
  </ul>
</ul>
<p>* Remark: there is a typo in backend .py. The named "node" variables and functions should actually mean "edge" of the network.</p>
<hr>
<h4>Provision service</h4>
<ol>
  <h4>frontend</h4>
  <li>Run 'npm install' on folder ./frontend to install package required by ReactJS</li>
  <li>Run 'npm run dev' to start server</li>
</ol>
<ol>
  <h4>Flask</h4>
  <li>Run python app.py on ./backend</li>
  <ul>
    <li><em>pip is required to install various packages used</em></li>
  </ul>
</ol>
<br>
<p><em>For the puprpose of demonstration, the repo is designed to work with the tables in the ./Sample Data folder</em>


