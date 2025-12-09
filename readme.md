<!DOCTYPE markdown>
<html>
<head>
</head>
<body>

<div id="Draconus">
    <h1 align="center">Draconus</h1>
    <p align="center">
        <img src="img/logo1.webp" alt="Logo Projektu" width="300">
    </p>
    <h4 align="center">Every USER should have a Cyber Weapon to defend himself.</h4>
    <p align="center">This project serves as a comprehensive toolkit designed to introduce fundamental concepts in ethical hacking and malware creation. It offers tools and functionalities for creating shellcodes, basic malware, code obfuscation, and code packing into single lines, providing an engaging way to explore malware techniques responsibly.</p>
    <h2>Features and Advantages</h2>
    <ul>
    <li><strong>Cross-Compilation Environment</strong>: Includes a custom Docker image preloaded with compilers for Assembly, C, C++, PyInstaller, and Nuitka, allowing seamless creation of Windows executables directly from Linux.</li>
    <li><strong>Flexible Server Framework</strong>: Provides multiple listener types with a lightweight management system to handle connections, file transfers, raw byte streams, and advanced command-based communication.</li>
    <li><strong>Executable Building from Source</strong>: Every EXE or DLL is generated starting from raw code, ensuring each build is unique and minimizing static signatures that appear in typical compiled malware.</li>
    <li><strong>Support for Complex Dependencies</strong>: Easily builds executables that require additional static or dynamic libraries. The build system automatically resolves and packages dependencies.</li>
    <li><strong>Modular Build System</strong>: Allows constructing EXEs and libraries in a layered fashion—one library can depend on another, and everything can be bundled into the final executable without user-side complexity.</li>
    <li><strong>Payload Creation Toolkit</strong>: Enables building custom payloads—primarily in Python—using ready-to-use modules. No programming knowledge is required to assemble functional payloads.</li>
    <li><strong>Highly Customizable Architecture</strong>: Every executable or library is built from modular pieces, enabling endless combinations and permitting small, specialized, and stealthy builds.</li>
    <li><strong>Shellcode Generation</strong>: Create custom shellcode for experimentation, analysis, and chaining with other payloads.</li>
    <li><strong>Code Obfuscation & Packing</strong>: Offers tools to obfuscate Python and assembly code, pack scripts into a single line, and experiment with evasion techniques in a safe, educational environment.</li>
    <li><strong>Integrated C2 Framework</strong>: Features built-in command-and-control functionality with support for multiple simultaneous clients, automated tasks, and structured communication channels.</li>
    <li><strong>Designed for Learning & Experimentation</strong>: Draconus is built as a safe playground for exploring malware techniques, cross-compilation, payload design, shellcoding, and low-level Windows/Linux internals.</li>
</ul>
<div>
<div id="Disclaimer">
    <h2>Disclaimer</h2>
    <p>
    <strong>This toolkit is developed solely for ethical and educational purposes to deepen understanding of malware creation and analysis. Using this tool to target other users, conduct attacks without prior consent, or apply it in unauthorized environments is strictly forbidden. The responsibility for proper use rests entirely on the user. Caution is advised! Misuse could harm your system or other users. We highly recommend using this tool within isolated virtual machines.</strong>
    </p>
</div>

</body>
</html>