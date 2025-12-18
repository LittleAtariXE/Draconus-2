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
<div id="About">
    <h2>About</h2>
    <p>
    Draconus is composed of two core components that work together to create a flexible, modular experimentation environment.
    </p>
    <p>
    <strong>Draconus</strong> itself runs quietly in the background, creating servers, managing connections, and handling all automated tasks. Once launched, it can operate indefinitely without user interaction, maintaining listeners and managing clients on its own.
    </p>
    <p>
    The second component, <strong>Commander</strong>, serves as the interactive interface for communicating with the background service. Through a console-style command system built with Python Click, users can issue commands, manage servers, inspect connections, and generate payloads.
    </p>
    <p>
    Commander also provides access to the <strong>Hive</strong> section, a workspace dedicated to creating payloads, modules, shellcode, and various building blocks used throughout the project. Hive simplifies the creation process, enabling users to assemble complex components from ready-made modules.
    </p>
    <p>
    Although Draconus is not as advanced or extensive as large-scale professional frameworks such as Metasploit, it takes inspiration from some of their ideas. The project is developed as a hobby initiative, exploring different approaches, techniques, and learning opportunities. Features like shellcode generation and payload embedding are present, but implemented in a way suited to the project’s unique design and philosophy.
    </p>
</div>
<div id="Contents">
    <h2>Contents</h2>
    <ul>
        <li><a href="#Draconus">Draconus</a></li>
        <li><a href="#Disclaimer">Disclaimer</a></li>
        <li><a href="#About">About</a></li>
        <li><a href="#Install">Install</a></li>
        <li><a href="#Start">Start</a></li>
        <li><a href="#FirstRun">First Run</a></li>
        <li><a href="#About">About</a></li>
        <li><a href="#About">About</a></li>
    </ul>
</div>
<div id="Install">
    <h2>Installation</h2>
    <ol>
        <li>Ensure you have Python 3.11.2 or a newer version installed on your system.</li>
        <li>Install Docker (e.g., using the following command):
            <pre><code>sudo apt install docker.io</code></pre>
        </li>
        <li>To allow the program to interact with Docker, you need to set the appropriate permissions. Run:
            <pre><code>sudo usermod -aG docker $USER</code></pre>
            Afterward, log out and back in (or restart your system) to apply the new permissions.
        </li>
        <li>Due to the recent policy changes in Python modules on Linux, make sure you have Python’s virtual environment package, <code>venv</code>, installed. If not, install it with:
            <pre><code>sudo apt install python3.11-venv</code></pre>
        </li>
    </ol>
    <p>The installation is complete, and your environment is ready to use.</p>
</div>
<div id="Start">
    <h2>Start</h2>
    <p>
    Before launching Draconus for the first time, review the <strong>CONFIG.ini</strong> file. This file defines the core runtime parameters of the project. One of the most important settings is the <strong>IP</strong> value, which should be set to your machine’s IP address. It will be used automatically when generating servers and payloads.  
    </p>
    <p>
    The configuration file also allows you to customize message colors, adjust maximum console width, and modify various other visual and functional options. All available parameters are documented directly inside the file.
    </p>
    <h3>1. Starting Draconus</h3>
    <p>
    The main background service is <strong>Draconus</strong>. It is designed to run continuously and independently, either in a separate console window or in the background.  
    </p>
    <p>
    To start it normally, run:
    </p>
    <pre><code>python3 Draconus.py</code></pre>
    <p>
    During the first launch, a built-in loader will automatically create a virtual environment and install all required packages.
    </p>
    <p>
    To run Draconus in the background, you can use:
    </p>
    <pre><code>nohup python3 Draconus.py &amp;</code></pre>
    <p>
    Draconus will continue running until manually terminated.
    </p>
    <h3>2. Starting Commander</h3>
    <p>
    Once Draconus is running, you can launch the control interface: <strong>Commander</strong>.  
    The program will not start unless it detects an active Draconus instance.
    </p>
    <p>
    Start Commander using:
    </p>
    <pre><code>python3 c2.py</code></pre>
    <p>
    If the connection succeeds, you will see a confirmation message indicating that Commander has successfully linked with Draconus. From here, you can manage servers, inspect connections, and access the Hive section for creating payloads, modules, and shellcode.
    </p>
</div>
<div id="FirstRun">
    <h2>First Run</h2>
    <p>When you start Draconus, a directory named <code>OUTPUT</code> will appear in its main directory. This is a critical folder where Draconus stores its logs, downloaded files, created worms, and more. Do not delete this directory while the program is running. You can safely delete it only when both Draconus and Commander are stopped.</p>
    <h4>Contents of the <code>OUTPUT</code> Directory:</h4>
    <ul>
    <li>
        <strong>Logs</strong> - This folder contains log files. Every message displayed by Draconus is saved here, along with a timestamp. 
        Similarly, any message received from clients is also logged.
    </li>
    <li>
        <strong>Loot</strong> - This folder stores files downloaded from or sent by clients. It will contain subdirectories named after the IP addresses of clients, which will hold the files sent by them. 
        Think of the <code>Loot</code> folder as the treasure chest for files received from clients.
    </li>
    <li>
    <strong>Hive</strong> - This folder contains files related to worms, source code, shellcodes, and ready-to-use executables. 
    If you create a worm, it will be stored here.
    </li>
    <li>
        <strong>Links</strong> - This folder provides shortcuts to various useful resources in the project, so you don't have to search for them manually. 
        It includes:
        <ul>
        <li>A folder with icons where you can add your own icons and use them when creating worms.</li>
        <li>A shortcut to files where you can add custom code, for example, to payloads.</li>
        </ul>
  </li>
    </ul>
    <h3>Using Commands</h3>
    <p>
        This README does not describe every Draconus command in detail, because the program itself provides extensive,
        built-in documentation.  
    </p>
    <p>
        By typing <code>help</code> inside Commander, you will see a full list of available commands together with their explanations.
        Many commands also include additional documentation available through the <code>--help</code> parameter, for example:  
    </p>
    <pre><code>server --help</code></pre>
    <p>
        This will show descriptions of available server types, their parameters, and usage examples.
    </p>
    <p>
        Each connected client is automatically assigned a unique ID.  
        To interact directly with a client, simply use:
    </p>
    <pre><code>conn &lt;ID&gt;</code></pre>
    <p>
        All of this is clearly documented inside the built-in help system.
    </p>
    <p>
        The <strong>Hive</strong> section, which will be described later in this README, is more advanced than the basic command layer.
        Since Hive enables building payloads, modules, shellcode, worms, and more, its structure and commands are explained here in additional detail.
    </p>
</div>
<div id="Hive">
    <h2>Hive</h2>
    <p>
        The <strong>Hive</strong> section is the creative core of Draconus.  
        It is the workspace where worms, payloads, modules, shellcode, and other components are designed and assembled.
        Draconus allows building a wide range of artifacts, from simple Python scripts to fully compiled Windows executables,
        dynamic libraries, and raw assembly shellcode.
    </p>
    <p>
        All created worms, payloads, and build artifacts are stored in the <code>OUTPUT/Hive</code> directory.
        Hive also supports saving completed projects as reusable payloads and placing them into an internal library,
        enabling flexible build combinations and rapid experimentation.
    </p>
    <p>
        The build process is intentionally simplified.  
        Even without programming knowledge, users can create custom payloads, executables, DLLs, or shellcode
        by assembling ready-made components. Many Hive commands include their own built-in documentation;
        simply append the <code>--help</code> parameter to any command to see usage instructions and available options.
    </p>
    <h3>Module Types</h3>
    <p>
        Hive is built around different module types, each serving a specific role in the construction process:
    </p>
    <ul>
        <li>
            <strong>worm</strong>  
            The primary module and the starting point of every project.  
            It defines the type of worm being created, such as shellcode, Python script, standalone executable, or DLL.
            The selected worm type determines whether additional modules or payloads can be embedded.
        </li>
        <li>
            <strong>module</strong>  
            Optional extensions that enhance or modify the behavior of a worm.  
            Not every worm template supports modules, while some templates are built entirely from modular components.
            Modules may consist of raw code snippets, dynamic DLLs, or static libraries.
        </li>
        <li>
            <strong>payload</strong>  
            Prebuilt functional components written in various languages.
            Worms or modules may expose dedicated injection points for payloads.
            Payloads are handled differently by the build system than modules,
            which is why similar functionality may exist in both forms.
        </li>
        <li>
            <strong>shadow</strong>  
            Code obfuscation components.  
            These modules transform source code into a heavily obscured and difficult-to-analyze form.
        </li>
        <li>
            <strong>scode</strong>  
            Templates for the shellcode generator.
            This category contains predefined shellcode types that can be generated on demand.
            Generated shellcode is exported in three popular formats for easy integration.
        </li>
        <li>
            <strong>food</strong>  
            Supporting data used by worms and modules.
            This includes text databases, link collections, naming resources, and specialized string sequences
            required by certain libraries.  
            Draconus uses <code>food</code> when generating application names, descriptions,
            metadata, and other contextual elements.
        </li>
    </ul>
</div>
</body>
</html>