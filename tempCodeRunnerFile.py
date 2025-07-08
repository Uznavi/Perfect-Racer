def playScreen():
    #TODO: Since this is the meat and bones of the game, try to make it clearer what is an object and what is the object update function
    pygame.display.set_caption("Game")
    pygame.mixer.music.load("assets/sounds/gameSong.mp3")
    pygame.mixer.music.play(-1)
    run = True
    lastUpdate = pygame.time.get_ticks()
    frame = 0
    score = 0
    showHitboxes = False

    #Game objects
    player = PlayerCar()
    enemy_spawner = EnemySpawner()
    # item_box = ItemBox()
    itemBox_spawner = ItemBoxSpawner()
    spriteGroup = pygame.sprite.Group()
    spriteGroup.add(player)

    while run:
        screen.fill((50,50,50))
        clock.tick(fps)
        score +=1

        currentTime = pygame.time.get_ticks()
        if currentTime - lastUpdate >= animationCooldown:
            frame +=1
            lastUpdate = currentTime
            if frame >= len(animationList):
                frame = 0
        screen_width, screen_height = screen.get_size()
        frame_image = animationList[frame]
        x = (screen_width - frame_image.get_width()) // 2
        y = (screen_height - frame_image.get_height()) // 2
        screen.blit(frame_image, (x, y))
        drawText(f"Score: {score}", 20, textColor, 1025, 450)
        if player.powerUpReceived != None:
            drawText(f"Power Up : {player.powerUpReceived}", 15, textColor, 1010, 475)

        #Game over cause
        if pygame.sprite.spritecollideany(player, enemy_spawner.enemy_group):
            if player.shieldActive:
                player.shieldActive = False
                player.shieldCoolDownTimer = 60
            elif player.bulletsActive:
                player.bulletsActive = False
                player.shieldCoolDownTimer = 60
            elif player.shieldCoolDownTimer == 0:
                gameOverScreen(score)
        

        #Item box hitting logic
        item_box_hit = pygame.sprite.spritecollideany(player, itemBox_spawner.itemBox_group)
        if item_box_hit:
            if not player.shieldActive:
                player.powerUpReceived = item_box_hit.powerUp
            if not player.bulletsActive:
                player.powerUpReceived = item_box_hit.powerUp
            item_box_hit.kill()
        
        if player.shieldActive:
            shieldSurface = pygame.Surface((player.rect.width*2, player.rect.height*2), pygame.SRCALPHA)
            pygame.draw.ellipse(
                shieldSurface,
                (100, 200, 255, 120),
                shieldSurface.get_rect()
            )
            shield_rect = shieldSurface.get_rect(center = player.rect.center)
            screen.blit(shieldSurface, shield_rect)
        
        if showHitboxes:        
            for enemy in enemy_spawner.enemy_group:
                pygame.draw.rect(screen, (255,0,0), enemy.rect, 2)
                pygame.draw.rect(screen, (0,255,0), player.rect, 2)

        action, showHitboxes = eventHandler.handle_gameplay_events(player, showHitboxes)
        if action == "quit":
            pygame.quit()
            sys.exit()
        elif action == "pause":
            result = pauseScreen()
            if result == "quit":
                pygame.quit()
                sys.exit()

        spriteGroup.draw(screen)
        spriteGroup.update()
        player.bullets.draw(screen)
        enemy_spawner.enemy_group.draw(screen)
        enemy_spawner.update()
        itemBox_spawner.itemBox_group.draw(screen)
        itemBox_spawner.update()
        pygame.display.update()