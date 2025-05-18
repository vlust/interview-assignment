#![no_std]
#![no_main]

use panic_halt as _;

use arduino_hal::pins;


// ADS1x1x driver (v0.3.0). We only need `Ads1x1x::new_ads1115`, `FullScaleRange`, `DataRate16Bit`, and `TargetAddr`.
use ads1x1x::{
    Ads1x1x,
    channel::DifferentialA0A1,
    DataRate16Bit,
    FullScaleRange,
    TargetAddr,
};
#[arduino_hal::entry]
fn main() -> ! {
    let dp = arduino_hal::Peripherals::take().unwrap();

    let mut pins = pins!(dp);

    let mut serial = arduino_hal::default_serial!(dp, pins, 9_600);

    let mut led = pins.d13.into_output();


    let sda = pins.a4.into_pull_up_input();
    let scl = pins.a5.into_pull_up_input();


    let i2c = arduino_hal::I2c::new(dp.TWI, sda, scl, 100_000);


    let mut adc = Ads1x1x::new_ads1115(i2c, TargetAddr::Gnd);

    adc.set_full_scale_range(FullScaleRange::Within4_096V).unwrap();


    adc.set_data_rate(DataRate16Bit::Sps128).unwrap();

    const SHUNT_RESISTANCE_OHM: f32 = 100.0;

    arduino_hal::delay_ms(100);

    loop {


        let raw: i16 = adc.read(DifferentialA0A1).unwrap();


        let volts: f32 = (raw as f32) * 4.096_f32 / 32_768.0_f32;

        let current_a: f32 = volts / SHUNT_RESISTANCE_OHM;
        let current_ma: f32 = current_a * 1_000.0_f32;


        let centi_milliamp: i16 = (current_ma * 100.0_f32) as i16; // e.g. 1234 for 12.34 mA
        let whole: i16 = centi_milliamp / 100;                     // 12
        let fract: i16 = (centi_milliamp.abs() % 100) as i16;      // 34

        // ufmt::uwrite!(&mut serial, "I: ").unwrap();
        // ufmt::uwrite!(&mut serial, "{}", whole).unwrap();
        // ufmt::uwrite!(&mut serial, ".").unwrap();
        if fract < 10 {
            ufmt::uwrite!(&mut serial, "0").unwrap();
        }
        // ufmt::uwrite!(&mut serial, "{}", fract).unwrap();
        // ufmt::uwrite!(&mut serial, " mA\r\n").unwrap();

        // —————————————————————————————————————————————————————————————————————
        if current_ma < 4.0_f32 || current_ma > 20.0_f32 {
            led.toggle();
        } else {
            led.set_low();
        }


        arduino_hal::delay_ms(200);
    }
}
