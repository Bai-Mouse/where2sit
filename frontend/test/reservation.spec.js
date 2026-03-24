import { test, expect } from '@playwright/test';

test('user can reserve a room', async ({ page }) => {
  await page.goto('/');

  await page.click('text=Reserve');
  
  await expect(page.locator('text=Reservation successful')).toBeVisible();
});