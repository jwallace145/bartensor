jest.setMock('selenium-webdriver', webdriver);
// This file was generated using Selenium IDE
const tests = require("./commons.js");
global.Key = require('selenium-webdriver').Key;
global.URL = require('url').URL;
global.BASE_URL = configuration.baseUrl || 'http://127.0.0.1:8000';
let vars = {};
jest.setTimeout(300000);
describe("Default Suite", () => {
  it("wrong login", async () => {
    await tests["wrong login"](driver, vars);
    expect(true).toBeTruthy();
  });
});
beforeEach(() => {
  vars = {};
});
afterEach(async () => (cleanup()));