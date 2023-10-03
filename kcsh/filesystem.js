
class Tree_Object {
  #name;
  #parent;

  constructor(name, parent = null) {
    this.#name = name;
    this.#parent = parent;
  }
  get name() {
    return this.#name;
  }
  get parent() {
    return this.#parent;
  }
  set parent(dir) {
    this.#parent = dir;
  }
}

class Directory extends Tree_Object {
  #contents;
  
  constructor(name, parent, contents = new Map()) {
    super(name, parent);
    this.#contents = contents;
  }
  print_contents() {
    const current_list = this.#contents;
    const sorted_keys = Array.from(current_list.keys()).sort();
    function format_dirs(x) {
      if (current_list.get(x) instanceof Directory) {
        return x + "/";
          }
      else {
        return x;
      }
    }
    return sorted_keys.map(format_dirs);
  }

  toString() {
    return this.#contents
  }
  
  insert(file_or_dir) {
    this.#contents.set(file_or_dir.name, file_or_dir);
    file_or_dir.parent = this;
  }

  remove(file_or_dir) {
    this.#contents.delete(file_or_dir);
  }

  contains(file_or_dir) {
    if (this.#contents.has(file_or_dir)) {
      return true;
    }
    else {
      return false;
    }
  }
  
  get_member(file_or_dir) {
    return this.#contents.get(file_or_dir);
  }
}

class File extends Tree_Object {
  #source;
  #file_type;
  
  constructor(name, parent, source = "", file_type = "text") {
    super(name, parent);
    this.#source = source;
    this.#file_type = file_type;
  }
  
  get source() {
    return this.#source;
  }

  get file_type() {
    return this.#file_type;
  }

  toString() {
    return this.#source;
  }
}

const filesystem = new Directory("/", null);


filesystem.insert(new Directory("home", null));
filesystem.insert(new Directory("dev", null));
filesystem.insert(new Directory("tmp", null));
const home_dir = filesystem.get_member("home");
const dev_dir = filesystem.get_member("dev");
const tmp_dir = filesystem.get_member("tmp");

home_dir.insert(new File("cat", null, "Meow Meow", "text"));
home_dir.insert(new File("linkedin", null, "https://www.linkedin.com/in/kaleb-crans/", "link"));
home_dir.insert(new File("github", null, "https://github.com/kcrans", "link"));
home_dir.insert(new File("resume", null, "https://kcrans.com/Resume_Kaleb_2022-6.pdf", "link"));
home_dir.insert(new Directory("projects", null));

dev_dir.insert(new File("src", null, "https://github.com/kcrans/kcrans.github.io", "link"));
dev_dir.insert(new File(".secret", null, "What band did some members of Uncle Tupelo start after that band split up?", "text"))

tmp_dir.insert(new File("now.txt", null, "Currently I'm getting cracked at liner algebra, working on ML projects, and learning about analog synths." , "text"));

var pointer = home_dir;
var last_pointer = home_dir;

console.log(filesystem.name);
console.log(filesystem.contains("home"));
console.log(filesystem.print_contents());
console.log(home_dir.print_contents());
console.log(home_dir.get_member("cat").source);
