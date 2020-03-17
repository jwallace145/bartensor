const utils = require("./utils.js");
const tests = {};
tests["wrong login"] = async (driver, vars, opts = {}) => {
  await driver.get("http://127.0.0.1:8000");
  vars["!statusOK"] = `true`;
  await driver.wait(until.elementLocated(By.id(`is21`)), configuration.timeout);
  await expect(driver.findElements(By.id(`is21`))).resolves.toBePresent();
  if (!!await driver.executeScript(`return (arguments[0])`, vars["!statusOK"])) {
    console.log(`modal found`);
    await driver.wait(until.elementLocated(By.id(`is21`)), configuration.timeout);
    await driver.findElement(By.id(`is21`)).then(element => {
      return element.click();
    });
  }
  await driver.wait(until.elementLocated(By.linkText(`Login`)), configuration.timeout);
  await driver.findElement(By.linkText(`Login`)).then(element => {
    return element.click();
  });
  await driver.wait(until.elementLocated(By.id(`id_username`)), configuration.timeout);
  await driver.findElement(By.id(`id_username`)).then(element => {
    return element.clear().then(() => {
      return element.sendKeys(`incorrect_username`);
    });
  });
  await driver.wait(until.elementLocated(By.id(`id_password`)), configuration.timeout);
  await driver.findElement(By.id(`id_password`)).then(element => {
    return element.clear().then(() => {
      return element.sendKeys(`password`);
    });
  });
  await driver.wait(until.elementLocated(By.css(`.btn-outline-info`)), configuration.timeout);
  await driver.findElement(By.css(`.btn-outline-info`)).then(element => {
    return element.click();
  });
  await driver.wait(until.elementLocated(By.css(`.border-top`)), configuration.timeout);
  await driver.findElement(By.css(`.border-top`)).then(element => {
    return element.click();
  });
  await driver.wait(until.elementLocated(By.css(`li`)), configuration.timeout);
  await expect(driver.findElements(By.css(`li`))).resolves.toBePresent();
}
tests["about page exists"] = async (driver, vars, opts = {}) => {
  await driver.get((new URL(`/`, BASE_URL)).href);
  vars["!statusOK"] = `true`;
  await driver.wait(until.elementLocated(By.id(`is21`)), configuration.timeout);
  await expect(driver.findElements(By.id(`is21`))).resolves.toBePresent();
  if (!!await driver.executeScript(`return (arguments[0])`, vars["!statusOK"])) {
    console.log(`modal found`);
    await driver.wait(until.elementLocated(By.id(`is21`)), configuration.timeout);
    await driver.findElement(By.id(`is21`)).then(element => {
      return element.click();
    });
  }
  await driver.wait(until.elementLocated(By.linkText(`About`)), configuration.timeout);
  await driver.findElement(By.linkText(`About`)).then(element => {
    return element.click();
  });
  await driver.wait(until.elementLocated(By.css(`.col-md-12 > .text-light:nth-child(1)`)), configuration.timeout);
  await expect(driver.findElements(By.css(`.col-md-12 > .text-light:nth-child(1)`))).resolves.toBePresent();
  await driver.wait(until.elementLocated(By.css(`.col-12:nth-child(1) > .cnt-block`)), configuration.timeout);
  await expect(driver.findElements(By.css(`.col-12:nth-child(1) > .cnt-block`))).resolves.toBePresent();
  await driver.wait(until.elementLocated(By.css(`.col-12:nth-child(2) > .cnt-block`)), configuration.timeout);
  await expect(driver.findElements(By.css(`.col-12:nth-child(2) > .cnt-block`))).resolves.toBePresent();
  await driver.wait(until.elementLocated(By.css(`.col-12:nth-child(3) > .cnt-block`)), configuration.timeout);
  await expect(driver.findElements(By.css(`.col-12:nth-child(3) > .cnt-block`))).resolves.toBePresent();
  await driver.wait(until.elementLocated(By.css(`.col-12:nth-child(4) > .cnt-block`)), configuration.timeout);
  await expect(driver.findElements(By.css(`.col-12:nth-child(4) > .cnt-block`))).resolves.toBePresent();
  await driver.wait(until.elementLocated(By.css(`.col-12:nth-child(5) > .cnt-block`)), configuration.timeout);
  await expect(driver.findElements(By.css(`.col-12:nth-child(5) > .cnt-block`))).resolves.toBePresent();
}
tests["how do i make a white russian"] = async (driver, vars, opts = {}) => {
  await driver.get((new URL(`/`, BASE_URL)).href);
  vars["!statusOK"] = `true`;
  await driver.wait(until.elementLocated(By.id(`is21`)), configuration.timeout);
  await expect(driver.findElements(By.id(`is21`))).resolves.toBePresent();
  console.log(`${vars.!statusOK}`);
  if (!!await driver.executeScript(`return (arguments[0])`, vars["!statusOK"])) {
    console.log(`modal found`);
    await driver.wait(until.elementLocated(By.id(`is21`)), configuration.timeout);
    await driver.findElement(By.id(`is21`)).then(element => {
      return element.click();
    });
  }
  await driver.wait(until.elementLocated(By.name(`search_bar`)), configuration.timeout);
  await driver.findElement(By.name(`search_bar`)).then(element => {
    return element.click();
  });
  await driver.wait(until.elementLocated(By.name(`search_bar`)), configuration.timeout);
  await driver.findElement(By.name(`search_bar`)).then(element => {
    return element.clear().then(() => {
      return element.sendKeys(`white russian`);
    });
  });
  await driver.wait(until.elementLocated(By.name(`search_bar`)), configuration.timeout);
  await driver.findElement(By.name(`search_bar`)).then(element => {
    return element.sendKeys(Key["ENTER"]);
  });
  await driver.wait(until.elementLocated(By.xpath(`(//button[@type=\'button\'])[2]`)), configuration.timeout);
  await driver.findElement(By.xpath(`(//button[@type=\'button\'])[2]`)).then(element => {
    return element.click();
  });
  await driver.wait(until.elementLocated(By.xpath(`(//button[@type=\'button\'])[2]`)), configuration.timeout);
  await expect(driver.findElements(By.xpath(`(//button[@type=\'button\'])[2]`))).resolves.toBePresent();
  await driver.wait(until.elementLocated(By.css(`#header1 img`)), configuration.timeout);
  await expect(driver.findElements(By.css(`#header1 img`))).resolves.toBePresent();
}
module.exports = tests;