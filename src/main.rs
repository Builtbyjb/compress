#[macro_use]
extern crate rocket;

pub mod utills;
use crate::utills::vid_convert::vid_convert;

use rocket::form::Form;
use rocket::fs::{relative, FileServer};

#[derive(FromForm)]
struct Num {
    num1: u32,
    num2: u32,
}

#[derive(Responder)]
#[response(status = 200, content_type = "json")]
struct Value(String);

#[post("/", format = "multipart/form-data", data = "<nums>")]
fn add_num(nums: Form<Num>) -> Value {
    let value: u32 = vid_convert(nums.num1, nums.num2);
    Value(format!("value: {}", value))
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
