#[macro_use]
extern crate rocket;
use rocket::form::Form;
use rocket::fs::{relative, FileServer};

#[derive(FromForm)]
struct Num {
    num1: u32,
    num2: u32,
}

#[post("/", format = "multipart/form-data", data = "<nums>")]
fn add_num(nums: Form<Num>) {
    println!("{}", nums.num1 + nums.num2);
}

// #[get("/<name>")]
// fn index(name: &str) -> String {
//     format!("Hello, {}", name)
// }

#[launch]
fn rocket() -> _ {
    rocket::build()
        .mount("/", routes![add_num])
        .mount("/", FileServer::from(relative!("static")))
}
