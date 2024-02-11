function play_audio(file_path, callback) {
  const sample = new Audio(file_path);
  sample.addEventListener("ended", callback);
  sample.play();
}

function ready(green_text) {
  const term = jQuery('#terminal').terminal({
    /* greetings: function(callback) {
      var text = "Take a look around?";
      this.echo(text);
      callback(console.log("Ran a greeting"));
    }, */
    vi: function(value) {    
      this.error("Error: Vi not found \nTry Vim instead");
    },
    echo: function(input) {
      const some_text = String(input);
      const str_length = some_text.length;
      const message = `${"echo\n".repeat(str_length)}${some_text}`;
      this.typing('echo', 100, message, function() {return "ccvc"} );
    },
    ls: function(...optional_dirs) {
      var has_file = false;
      var has_error = false;
      var has_dir = false;
      if (optional_dirs.length == 1 && optional_dirs[0] == "-d") {
        const term_css = document.getElementById("terminal");
        term_css.id = "lsd_terminal";
        
        const cmd_css = document.getElementsByClassName("cmd")[0];
        
        const cmd_prompt_css = document.getElementsByClassName("cmd-prompt")[0];
        
        let green_css = document.getElementsByClassName("green_text");
        Array.from(green_css).forEach((element) => {
          element.classList.remove("green_text");
          element.classList.add("lsd_green_text");
        });
        green_text = "lsd_green_text";
        
        cmd_css.classList.add("lsd_cmd");
        cmd_prompt_css.classList.add("lsd_cmd_prompt");
        
        const lsd_img = new Image(200, 200);
        lsd_img.src = "lsd_search1.png";
        this.echo(lsd_img);
        this.echo("wait, that isn't a directory!!!");
        
        function clean_up() {
          term_css.id = "terminal";
          cmd_css.classList.remove("lsd_cmd");
          cmd_prompt_css.classList.remove("lsd_cmd_prompt");
          green_css = document.getElementsByClassName("lsd_green_text");
          Array.from(green_css).forEach((element) => {
            element.classList.remove("lsd_green_text");
            element.classList.add("green_text");
          });
          green_text = "green_text";
        }
        
        play_audio("Starting_Over.mp3", clean_up);
        //term_css.id = "terminal";
        //console.log(style.getPropertyValue("--color"));
      }
      else if (optional_dirs.length > 0) {
        for (const file_or_dir of optional_dirs) {
          if (!pointer.contains(file_or_dir)) {
            this.echo(`ls: ${file_or_dir}: No such file or directory`);
            has_error = true;
          }
        }
        for (const file_or_dir of optional_dirs) {
          if (pointer.contains(file_or_dir) && pointer.get_member(file_or_dir) instanceof File) {
            this.echo(`${pointer.get_member(file_or_dir).name}`);
            has_file = true;
          }
        }
        const dirs = [];
        for (const file_or_dir of optional_dirs) {
          if (pointer.contains(file_or_dir) && pointer.get_member(file_or_dir) instanceof Directory) {
            const sub_dir = pointer.get_member(file_or_dir);
            dirs.push(sub_dir);
          }
        }
        if (has_file && dirs.length > 0) {
          this.echo(""); // Blank line if there are files followed by directories
        }
        if (dirs.length == 1) { // Special case when there is only one directory:
          if (has_error || has_file) { // You might not need to print the name of the directory
            this.echo(`${dirs[0].name}:`);
          }
          dirs[0].print_contents().forEach((x) => this.echo(x));
        }
        else {
          for (const dir of dirs) {
            if (has_dir) { // This is just so the first directory listed doesn't get two blank lines
              this.echo("");
            }
            this.echo(`${dir.name}:`);
            dir.print_contents().forEach((x) => this.echo(x));
            has_dir = true;
          }
        }
      }
      else {
        pointer.print_contents().forEach((x) => this.echo(x)); // Case where no args given
      }
    },
    exit: function() {
      this.echo("bye bye");
      setTimeout(function() {
            window.location.href = '/';
      }, 2000); // Wait 2000ms before exiting. Gives enough time to read goodbye message.
    },
    help: function() {
      this.echo("Try some basic UNIX commands: \n ls: print current directory contents \n cd: change directory \n cat: read a file \n exit: close terminal and return to homepage")
    },
    cd: function(where) {
      if (where === undefined) {
        last_pointer = pointer;
        pointer = home_dir;
        this.echo("back to where it all started, back to the home directory");
      }
      else if (where == ".") {
        this.echo("nothing changed");
      }
      else if (where == "..") {
        if (pointer.parent != null) {
          last_pointer = pointer;
          pointer = pointer.parent;
        }
        else {
          this.echo("already at root")
        }
      }
      else if (where == "-") {
        var temp_pointer = pointer;
        pointer = last_pointer;
        last_pointer = temp_pointer;
      }
      else {
        if (pointer.contains(where)) {
          if (pointer.get_member(where) instanceof Directory) {
            last_pointer = pointer;
            pointer = pointer.get_member(where);
          }
          else {
            this.echo(`cd: not a directory: ${where}`)
          }
        }
        else {
          this.echo(`cd: no such file or directory: ${where}`)
        }
      }
    },
    lcd: function(where) {
      this.echo(`${where}? I was there`);
    },
    pwd: function() {
      this.echo("uh just look at the prompt to the left of '%'");
    },
    wilco: function() {
      play_audio("yhf.mp3");
    },
    mkdir: function() {
      this.error("Error: This filesystem is read-only");
    },
    cp: function() {
      this.error("Error: This filesystem is read-only");
    },
    mv: function() {
      this.error("Error: This filesystem is read-only");
    },
    cat: function(...optional_args) {
      if (optional_args.length == 0) {
        const cat_img = new Image(400, 400);
        cat_img.src = "mittens_sophie_scaled.png";
        this.echo(cat_img);
        this.echo("meow");
      }
      else {
        for (const file_name of optional_args) {
          if (pointer.contains(file_name)) {
            const file = pointer.get_member(file_name);
            if (file instanceof File) {
              if (file.file_type == "text") {
                this.echo(file.source);
              }
              else if (file.file_type == "link") {
                const link = $('<a>', {text: file_name, href: file.source});
                this.echo(link);
              }
            }
            else {
              this.echo(`cat: ${file_name}: Is a directory`)
            }
          }
          else {
            this.echo(`cat: ${file_name}: No such file or directory`);
          }
        }
      }
    },
    touch: function(...optional_args) {
      if (optional_args.length == 0)
        this.echo("one touch is never enough");
      else {
        this.error("Error: This filesystem is read-only");
      }
    },
    waste: function(...optional_args) {
        const horn_img = new Image(30, 20);
        horn_img.src = "horn.jpg";
        this.echo(horn_img);

    },
    rm: function(...optional_args) {
      if (optional_args.length == 0)
        this.error("usage: rm [-f | -i] [-dIPRrvWx] file ...\n       rmunlink [--] file");
      else {
        this.error("not so fast");
      }
    
    },
    vim: function(...optional_args) {
      if (optional_args.length == 0) {
        var vim_text = document.createElement("span");
        vim_text.id = "vim";
        vim_text.classList.add(green_text);
        var text = document.createTextNode("VIM - Vi IMproved\ntry opening a file");
        vim_text.appendChild(text);
        this.echo(vim_text);
      }
      else {
        this.error("hahaha, you are trapped🔒");
        var counter = 0;
        this.push(function(command) {
            command = command.trim();
            if (command == "q" || command == "wq" || command == "q!" || command == "wqa")
            {
                term.echo("whaaaaaat? this wasn't suppose to be easy");
                term.pop();
            }
          else {
            // console.log(counter);
            ++counter;
            if (counter == 3) {
              const way_out = new Image(300, 203);
              way_out.src = "first-contact-way.png";
              way_out.alt = "Hint: use q! to exit vim!";
              way_out.title = "Credit to @caseyjohnellis for this image";
              term.echo(way_out);
            }
            else
              term.error("try again if you dare");
          }
        },
                {prompt: ":",
                name: "vi"});
    }}
  }, {
        checkArity: false,
        greetings: false,
        onInit() {
          this.echo(render_art());
          var intro_text = document.createElement("span");
          intro_text.id = "greetings";
          intro_text.classList.add(green_text);
          var text = document.createTextNode("\nhi, take a look around. type 'help' for more info.");
          intro_text.appendChild(text);
          
          this.echo(intro_text);
          //this.echo(`\n[[;rgba(78,154,6,0.99);]hi, take a look around. type 'help' for more info.]`);
        },
        prompt: () => {return `user@kcrans.com ${pointer.name} % `}});
}
function render_art() {
  ascii_art = `
88                               88
88                               88
88                               88
88   ,d8   ,adPPYba,  ,adPPYba,  88,dPPYba,
88 ,a8"   a8"     ""  I8[    ""  88P'    "8a
8888[     8b           \`"Y8ba,   88       88
88\`"Yba,  "8a,   ,aa  aa    ]8I  88       88
88   \`Y8a  \`"Ybbd8"'  \`"YbbdP"'  88       88`
  return ascii_art;
}

ready("green_text");
